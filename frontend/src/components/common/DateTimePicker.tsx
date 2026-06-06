import { CalendarDays, X } from 'lucide-react'
import { useState } from 'react'

interface DateTimePickerProps {
  id: string
  label: string
  value?: string
  onChange: (value: string) => void
}

export function DateTimePicker({
  id,
  label,
  onChange,
  value = '',
}: DateTimePickerProps) {
  const [isOpen, setIsOpen] = useState(false)
  const [draftDate, setDraftDate] = useState('')
  const [draftTime, setDraftTime] = useState('12:00')

  function togglePicker() {
    if (!isOpen) {
      syncDraftFromValue()
    }

    setIsOpen((current) => !current)
  }

  function syncDraftFromValue() {
    const [date, time] = splitDateTime(value)
    setDraftDate(date)
    setDraftTime(time || '12:00')
  }

  function confirmSelection() {
    if (!draftDate) {
      onChange('')
      setIsOpen(false)
      return
    }

    onChange(`${draftDate}T${draftTime || '12:00'}`)
    setIsOpen(false)
  }

  function clearSelection() {
    setDraftDate('')
    setDraftTime('12:00')
    onChange('')
    setIsOpen(false)
  }

  return (
    <div className={`date-time-field ${isOpen ? 'open' : ''}`}>
      <label htmlFor={id}>{label}</label>
      <button
        className="date-time-trigger"
        id={id}
        type="button"
        onClick={togglePicker}
      >
        <span>{value ? formatDateTimeValue(value) : 'No due date'}</span>
        <CalendarDays size={17} />
      </button>

      {isOpen ? (
        <div className="date-time-popover">
          <div className="date-time-grid">
            <label>
              <span>Date</span>
              <input
                type="date"
                value={draftDate}
                onChange={(event) => setDraftDate(event.target.value)}
              />
            </label>
            <label>
              <span>Time</span>
              <input
                type="time"
                value={draftTime}
                onChange={(event) => setDraftTime(event.target.value)}
              />
            </label>
          </div>

          <div className="date-time-actions">
            <button className="button button-ghost" type="button" onClick={clearSelection}>
              <X size={16} />
              Clear
            </button>
            <button
              className="button button-ghost"
              type="button"
              onClick={() => setIsOpen(false)}
            >
              Cancel
            </button>
            <button className="button button-primary" type="button" onClick={confirmSelection}>
              OK
            </button>
          </div>
        </div>
      ) : null}
    </div>
  )
}

function splitDateTime(value: string) {
  if (!value) {
    return ['', ''] as const
  }

  const [date, time = ''] = value.split('T')
  return [date, time.slice(0, 5)] as const
}

function formatDateTimeValue(value: string) {
  const date = new Date(value)

  if (Number.isNaN(date.getTime())) {
    return value
  }

  return new Intl.DateTimeFormat(undefined, {
    dateStyle: 'medium',
    timeStyle: 'short',
  }).format(date)
}
