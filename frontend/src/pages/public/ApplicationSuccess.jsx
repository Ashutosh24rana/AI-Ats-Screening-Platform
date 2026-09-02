import { Link, useParams } from 'react-router-dom'

export default function ApplicationSuccess() {
  const { slug } = useParams()

  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-50 px-4">
      <div className="card max-w-md text-center">
        <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-green-100 text-3xl">
          ✓
        </div>
        <h1 className="mt-4 text-xl font-bold text-slate-800">Application submitted!</h1>
        <p className="mt-2 text-sm text-slate-500">
          Thank you for applying. Your resume has been received and will be analyzed by our AI screening
          system. The hiring team will review your application soon.
        </p>
        <Link to={`/apply/${slug}`} className="btn-secondary mt-6">
          Back to job posting
        </Link>
      </div>
    </div>
  )
}
