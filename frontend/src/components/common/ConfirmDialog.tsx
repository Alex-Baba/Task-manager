import { Trash2 } from 'lucide-react'

interface ConfirmDialogProps {
  confirmLabel?: string
  description: React.ReactNode
  isPending: boolean
  title: string
  onCancel: () => void
  onConfirm: () => void
}

export function ConfirmDialog({
  confirmLabel = 'Delete',
  description,
  isPending,
  onCancel,
  onConfirm,
  title,
}: ConfirmDialogProps) {
  return (
    <div className="modal-backdrop" role="presentation">
      <section
        aria-labelledby="confirm-dialog-title"
        aria-modal="true"
        className="modal"
        role="dialog"
      >
        <div>
          <h2 id="confirm-dialog-title">{title}</h2>
          <p>{description}</p>
        </div>

        <div className="modal-actions">
          <button
            className="button button-ghost"
            disabled={isPending}
            type="button"
            onClick={onCancel}
          >
            Cancel
          </button>
          <button
            className="button button-danger"
            disabled={isPending}
            type="button"
            onClick={onConfirm}
          >
            <Trash2 size={17} />
            {confirmLabel}
          </button>
        </div>
      </section>
    </div>
  )
}
