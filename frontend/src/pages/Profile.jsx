
import { useAuth } from '../context/AuthContext'
import { User, Mail, Phone, MapPin } from 'lucide-react'

function Profile() {
  const { user } = useAuth()

  const name = user?.full_name || 'Not available yet'
  const email = user?.email || 'Not available yet'
  const initial = user?.full_name?.charAt(0)?.toUpperCase() || 'U'

  return (
    <div className="page-content">
      <header className="page-header">
        <div>
          <p className="eyebrow">YOUR ACCOUNT</p>
          <h1>My Profile</h1>
          <p className="subtitle">View your personal information.</p>
        </div>
      </header>

      <section className="profile-card">
        <div className="profile-banner">
          <div className="profile-avatar">
            {initial}
          </div>
          <div>
            <h2>{name}</h2>
            <p>{email}</p>
          </div>
        </div>

        <div className="profile-form">
          <h2>Personal Information</h2>

          <label>Full Name</label>
          <div className="profile-input">
            <User size={18} />
            <input value={name} readOnly />
          </div>

          <label>Email Address</label>
          <div className="profile-input">
            <Mail size={18} />
            <input value={email} type="email" readOnly />
          </div>

          <label>Phone Number</label>
          <div className="profile-input">
            <Phone size={18} />
            <input value="Not available yet" readOnly />
          </div>

          <label>Location</label>
          <div className="profile-input">
            <MapPin size={18} />
            <input value="Not available yet" readOnly />
          </div>

          <p className="subtitle">
            Profile editing will be available once the backend profile endpoints are implemented.
          </p>
        </div>
      </section>
    </div>
  )
}

export default Profile
