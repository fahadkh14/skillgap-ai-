import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext'
import { ToastProvider } from './context/ToastContext'
import ProtectedRoute from './components/ProtectedRoute'
import ErrorBoundary from './components/ErrorBoundary'

import Landing from './pages/Landing'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import Profile from './pages/Profile'
import Skills from './pages/Skills'
import Resume from './pages/Resume'
import Analyze from './pages/Analyze'
import AnalysisDetail from './pages/AnalysisDetail'
import Roadmap from './pages/Roadmap'
import History from './pages/History'
import Settings from './pages/Settings'
import NotFound from './pages/NotFound'

export default function App() {
  return (
    <ErrorBoundary>
      <BrowserRouter>
        <AuthProvider>
          <ToastProvider>
            <Routes>
              <Route path="/" element={<Landing />} />
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />

              <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
              <Route path="/profile" element={<ProtectedRoute><Profile /></ProtectedRoute>} />
              <Route path="/skills" element={<ProtectedRoute><Skills /></ProtectedRoute>} />
              <Route path="/resume" element={<ProtectedRoute><Resume /></ProtectedRoute>} />
              <Route path="/analyze" element={<ProtectedRoute><Analyze /></ProtectedRoute>} />
              <Route path="/analysis/:id" element={<ProtectedRoute><AnalysisDetail /></ProtectedRoute>} />
              <Route path="/roadmap" element={<ProtectedRoute><Roadmap /></ProtectedRoute>} />
              <Route path="/history" element={<ProtectedRoute><History /></ProtectedRoute>} />
              <Route path="/settings" element={<ProtectedRoute><Settings /></ProtectedRoute>} />

              <Route path="*" element={<NotFound />} />
            </Routes>
          </ToastProvider>
        </AuthProvider>
      </BrowserRouter>
    </ErrorBoundary>
  )
}
