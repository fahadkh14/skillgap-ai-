import { useRef, useState } from 'react'
import AppLayout from '../layouts/AppLayout'
import resumeService from '../services/resumeService'
import skillService from '../services/skillService'
import { useToast } from '../context/ToastContext'

const PROFICIENCIES = ['Beginner', 'Intermediate', 'Advanced', 'Expert']

export default function Resume() {
  const fileInputRef = useRef(null)
  const [fileName, setFileName] = useState('')
  const [uploading, setUploading] = useState(false)
  const [detected, setDetected] = useState([])
  const [selected, setSelected] = useState({})
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')
  const { showToast } = useToast()

  const handleFileChange = async (e) => {
    const file = e.target.files[0]
    if (!file) return

    const ext = file.name.split('.').pop().toLowerCase()
    if (!['pdf', 'docx'].includes(ext)) {
      setError('Only PDF and DOCX files are supported.')
      return
    }
    if (file.size > 5 * 1024 * 1024) {
      setError('File is too large. Maximum size is 5 MB.')
      return
    }

    setError('')
    setFileName(file.name)
    setUploading(true)
    setDetected([])

    try {
      const result = await resumeService.uploadResume(file)
      setDetected(result.detected_skills)
      const initialSelection = {}
      result.detected_skills.forEach((s) => { initialSelection[s] = true })
      setSelected(initialSelection)
      if (result.detected_skills.length === 0) {
        showToast('Resume processed — no known skills detected', 'info')
      } else {
        showToast(`Detected ${result.detected_skills.length} skill(s)`, 'success')
      }
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to process resume')
    } finally {
      setUploading(false)
    }
  }

  const toggleSkill = (skill) => {
    setSelected((s) => ({ ...s, [skill]: !s[skill] }))
  }

  const handleAddSelected = async () => {
    const skillsToAdd = detected.filter((s) => selected[s])
    if (skillsToAdd.length === 0) return
    setSaving(true)
    let addedCount = 0
    for (const skillName of skillsToAdd) {
      try {
        await skillService.addSkill({ skill_name: skillName, proficiency: 'Intermediate', years_of_experience: 0 })
        addedCount += 1
      } catch {
        // Skip skills that already exist or fail validation; continue with the rest
      }
    }
    setSaving(false)
    showToast(`Added ${addedCount} skill(s) to your profile`, 'success')
    setDetected([])
    setSelected({})
    setFileName('')
  }

  return (
    <AppLayout title="Resume">
      <div className="card mb-4">
        <h3>Upload your resume</h3>
        <p className="text-muted text-sm">PDF or DOCX, up to 5 MB. We only extract skill mentions — your resume content is never stored.</p>

        <div
          onClick={() => fileInputRef.current?.click()}
          style={{
            border: '2px dashed var(--color-border-strong)',
            borderRadius: 'var(--radius-md)',
            padding: '32px',
            textAlign: 'center',
            cursor: 'pointer',
            background: 'var(--color-surface-sunken)',
          }}
        >
          <p style={{ margin: 0, fontWeight: 600 }}>{fileName || 'Click to choose a file'}</p>
          <p className="text-faint text-sm" style={{ margin: 0 }}>or drag and drop here</p>
          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf,.docx"
            style={{ display: 'none' }}
            onChange={handleFileChange}
          />
        </div>

        {uploading && <p className="text-muted text-sm mt-2">Processing resume…</p>}
        {error && <div className="form-error mt-2">{error}</div>}
      </div>

      {detected.length > 0 && (
        <div className="card">
          <h3>Skills detected from your resume</h3>
          <p className="text-muted text-sm">Review and approve which skills to add. Nothing is added automatically.</p>
          <div className="flex-col gap-2 mt-4">
            {detected.map((skill) => (
              <label key={skill} className="flex items-center gap-3" style={{ padding: '8px 0' }}>
                <input type="checkbox" checked={!!selected[skill]} onChange={() => toggleSkill(skill)} />
                {skill}
              </label>
            ))}
          </div>
          <button className="btn btn-accent mt-4" onClick={handleAddSelected} disabled={saving}>
            {saving ? 'Adding…' : 'Add selected skills'}
          </button>
        </div>
      )}
    </AppLayout>
  )
}
