import { useForm } from 'react-hook-form'

import { EMPLOYMENT_TYPES } from '../../utils/constants'

export default function JobForm({ initialData, onSubmit, submitting, submitLabel = 'Save Job' }) {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({
    defaultValues: {
      title: '',
      description: '',
      required_skills: '',
      preferred_skills: '',
      minimum_experience: 0,
      location: '',
      employment_type: 'FULL_TIME',
      ...initialData,
    },
  })

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="card space-y-4">
      <div>
        <label className="label" htmlFor="title">Job Title</label>
        <input
          id="title"
          className="input-field"
          placeholder="Senior Backend Engineer"
          {...register('title', { required: 'Title is required' })}
        />
        {errors.title && <p className="mt-1 text-xs text-red-600">{errors.title.message}</p>}
      </div>

      <div>
        <label className="label" htmlFor="description">Job Description</label>
        <textarea
          id="description"
          rows={7}
          className="input-field"
          placeholder="Describe the role, responsibilities, and what a great candidate looks like..."
          {...register('description', { required: 'Description is required' })}
        />
        {errors.description && <p className="mt-1 text-xs text-red-600">{errors.description.message}</p>}
      </div>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <div>
          <label className="label" htmlFor="required_skills">Required Skills (comma-separated)</label>
          <input
            id="required_skills"
            className="input-field"
            placeholder="Python, FastAPI, PostgreSQL"
            {...register('required_skills', { required: 'At least one required skill' })}
          />
          {errors.required_skills && <p className="mt-1 text-xs text-red-600">{errors.required_skills.message}</p>}
        </div>
        <div>
          <label className="label" htmlFor="preferred_skills">Preferred Skills (comma-separated)</label>
          <input
            id="preferred_skills"
            className="input-field"
            placeholder="Docker, AWS, React"
            {...register('preferred_skills')}
          />
        </div>
      </div>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
        <div>
          <label className="label" htmlFor="minimum_experience">Min Experience (years)</label>
          <input
            id="minimum_experience"
            type="number"
            min="0"
            max="40"
            className="input-field"
            {...register('minimum_experience', { valueAsNumber: true, min: 0 })}
          />
        </div>
        <div>
          <label className="label" htmlFor="location">Location</label>
          <input
            id="location"
            className="input-field"
            placeholder="Remote / New York"
            {...register('location', { required: 'Location is required' })}
          />
          {errors.location && <p className="mt-1 text-xs text-red-600">{errors.location.message}</p>}
        </div>
        <div>
          <label className="label" htmlFor="employment_type">Employment Type</label>
          <select id="employment_type" className="input-field" {...register('employment_type')}>
            {EMPLOYMENT_TYPES.map((type) => (
              <option key={type.value} value={type.value}>
                {type.label}
              </option>
            ))}
          </select>
        </div>
      </div>

      <button type="submit" className="btn-primary" disabled={submitting}>
        {submitting ? 'Saving...' : submitLabel}
      </button>
    </form>
  )
}
