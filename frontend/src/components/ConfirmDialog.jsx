export default function ConfirmDialog({ open, title, message, confirmLabel = 'Confirm', onConfirm, onCancel, danger = true }) {
  if (!open) return null
  return (
    <div className="modal-overlay" role="dialog" aria-modal="true">
      <div className="modal">
        <h3>{title}</h3>
        <p className="text-muted text-sm">{message}</p>
        <div className="flex justify-between gap-3 mt-4">
          <button className="btn btn-secondary btn-block" onClick={onCancel}>Cancel</button>
          <button className={`btn ${danger ? 'btn-danger' : 'btn-primary'} btn-block`} onClick={onConfirm}>
            {confirmLabel}
          </button>
        </div>
      </div>
    </div>
  )
}
