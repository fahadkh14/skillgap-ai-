import { Component } from 'react'

export default class ErrorBoundary extends Component {
  constructor(props) {
    super(props)
    this.state = { hasError: false }
  }

  static getDerivedStateFromError() {
    return { hasError: true }
  }

  componentDidCatch(error, info) {
    console.error('SkillGap AI encountered an unexpected error:', error, info)
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="auth-shell">
          <div className="auth-card" style={{ textAlign: 'center' }}>
            <h2>Something went wrong</h2>
            <p className="text-muted">Please refresh the page and try again.</p>
            <button className="btn btn-primary mt-4" onClick={() => window.location.reload()}>
              Refresh
            </button>
          </div>
        </div>
      )
    }
    return this.props.children
  }
}
