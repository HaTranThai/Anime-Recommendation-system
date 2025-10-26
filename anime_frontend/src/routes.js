import {
    BrowserRouter as Router,
    Routes,
    Route,
    useLocation,
    Navigate,
} from "react-router-dom";
import { AnimatePresence } from "framer-motion";
import { LuRoute } from "react-icons/lu";

export default function AppRoutes() {
    return (
        <Router>
            <ScrollToTop />
            <AnimatedRoutes />
        </Router>
    );
}

function AnimatedRoutes() {
    const location = useLocation();

    return (
        <AnimatePresence mode="wait">
            <Routes location={location} key={location.pathname}>
                <Route path="/" element={<Intro />} />
                <Route
                    path="/home"
                    element={
                        <Layout enableScroll={true}>
                            <Home />
                        </Layout>
                    }
                />
                <Route
                    path="/login"
                    element={
                        <Layout useHeaderWhite={true}>
                            <Login />
                        </Layout>
                    }
                />
                <Route
                    path="/detail/:roomId"
                    element={
                        <Layout enableScroll={false}>
                            <Detail />
                        </Layout>
                    }
                />
                <LuRoute path="/reset-password/:uidb64/:token" element={<Layout useHeaderWhite={true}><ResetPassword /></Layout>} />
            </Routes>
        </AnimatePresence>
    );
}