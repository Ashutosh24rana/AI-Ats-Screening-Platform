import { Navigate, Route, Routes } from 'react-router-dom'

import Login from '../pages/auth/Login.jsx'
import Register from '../pages/auth/Register.jsx'
import DashboardLayout from '../components/layout/DashboardLayout.jsx'
import DashboardHome from '../pages/dashboard/DashboardHome.jsx'
import Jobs from '../pages/jobs/Jobs.jsx'
import CreateJob from '../pages/jobs/CreateJob.jsx'
import EditJob from '../pages/jobs/EditJob.jsx'
import JobDetails from '../pages/jobs/JobDetails.jsx'
import Candidates from '../pages/candidates/Candidates.jsx'
import CandidateDetails from '../pages/candidates/CandidateDetails.jsx'
import Home from '../pages/Home.jsx'
import JobApplication from '../pages/public/JobApplication.jsx'
import ApplicationSuccess from '../pages/public/ApplicationSuccess.jsx'
import ProtectedRoute from './ProtectedRoute.jsx'

export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />

      {/* Public candidate flow — no authentication, no accounts */}
      <Route path="/apply/:slug" element={<JobApplication />} />
      <Route path="/apply/:slug/success" element={<ApplicationSuccess />} />

      {/* Company auth */}
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />

      {/* Protected company dashboard */}
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <DashboardLayout />
          </ProtectedRoute>
        }
      >
        <Route index element={<DashboardHome />} />
        <Route path="jobs" element={<Jobs />} />
        <Route path="jobs/new" element={<CreateJob />} />
        <Route path="jobs/:jobId" element={<JobDetails />} />
        <Route path="jobs/:jobId/edit" element={<EditJob />} />
        <Route path="candidates" element={<Candidates />} />
        <Route path="candidates/:applicationId" element={<CandidateDetails />} />
      </Route>

      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}
