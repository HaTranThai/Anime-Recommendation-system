from .serializers import *
from django.shortcuts import render
from django.conf import settings
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView,
    CreateAPIView, UpdateAPIView, DestroyAPIView
)

from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.response import Response
import jwt

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class RegisterUserView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        try: 
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token

            response_data = {
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(access),
            }

            return Response(response_data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = UserTokenObtainPairSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user

        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        data = serializer.validated_data
        data.update({
            'refresh': str(refresh),
            'access': str(access),
        })

        return Response(data, status=status.HTTP_200_OK)

        
class UserDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
        
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logout successful."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class UpdateUserView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        fields_to_update = ['full_name', 'phone_number', 'age', 'gender']
        for field in fields_to_update:
            if field in request.data:
                setattr(user, field, request.data[field])
        user.save()
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)

        
class ChangePasswordView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(instance=user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'detail': 'Password changed successfully.'}, status=status.HTTP_200_OK)

class AddAnimeView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = AnimeSerializer

    def perform_create(self, serializer):
        serializer.save()

class AnimeListView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = AnimeSerializer
    queryset = Anime.objects.all()

class AnimeDetailView(RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = AnimeSerializer
    queryset = Anime.objects.all()

class DeleteAnimeView(DestroyAPIView):
    permission_classes = [AllowAny]
    serializer_class = AnimeSerializer
    queryset = Anime.objects.all()

class UserWatchListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = request.user.profile
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

class AddWatchHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, anime_id):
        try:
            profile = request.user.profile
            anime = Anime.objects.get(id=anime_id)
            history, _ = UserWatchHistory.objects.get_or_create(user_profile=profile, anime=anime)
            history.save()
            return Response({"message": f"Added {anime.title} to watch history"})
        except Anime.DoesNotExist:
            return Response({"error": "Anime not found"}, status=404)
        
class RecommendForUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # ✅ Lấy danh sách phim user đã xem
        watched_titles = list(
            user.profile.watched_animes.values_list("title", flat=True)
        )
        if not watched_titles:
            return Response(
                {"message": "User has not watched any anime yet."}, status=200
            )

        # ✅ Load dữ liệu embeddings và DataFrame
        try:
            df = pd.read_csv(
                r"C:\Users\ha200\MyWork\Study\Năm 4 Học Kì 1\RS\Project\RecommendAnime\anime_backend\anime_recommend\api\anime_data.csv"
            )
            combined_embs = np.load(
                r"C:\Users\ha200\MyWork\Study\Năm 4 Học Kì 1\RS\Project\RecommendAnime\anime_backend\anime_recommend\api\combined_embs.npy"
            )
        except Exception as e:
            return Response(
                {"error": f"Cannot load embedding files: {str(e)}"}, status=500
            )

        # ✅ Ánh xạ phim user đã xem sang index trong df
        indices = pd.Series(df.index, index=df["Title"]).drop_duplicates()
        watched_idx = [indices[t] for t in watched_titles if t in indices]

        if not watched_idx:
            return Response(
                {"message": "No watched titles found in dataset."}, status=200
            )

        # ✅ Tạo user embedding trung bình
        user_emb = np.mean(combined_embs[watched_idx], axis=0)
        user_emb = user_emb / np.linalg.norm(user_emb)

        # ✅ Tính cosine similarity
        sims = cosine_similarity([user_emb], combined_embs)[0]
        sims[watched_idx] = -1  # loại phim đã xem

        # ✅ Lấy top-N phim tương tự
        top_n = int(request.GET.get("top_n", 10))
        top_idx = sims.argsort()[::-1][:top_n]
        recs = df.iloc[top_idx]
        
        # print("✅ Recommended ID:", recs["ID"])
        
        recommended_animes = []

        for _, row in recs.iterrows():
            anime_id = row.get("ID") or row.get("id") or row.get("anime_code")

            if pd.isna(anime_id):
                continue 

            try:
                anime_id = int(anime_id)
            except (ValueError, TypeError):
                anime_id = str(anime_id).strip()

            anime = Anime.objects.filter(anime_code=anime_id).first()
            if anime:
                recommended_animes.append(anime)

        # print("✅ Matched anime codes:", [a.anime_code for a in recommended_animes])

        # ✅ Serialize kết quả
        serializer = AnimeSerializer(recommended_animes, many=True)
        return Response(serializer.data, status=200)