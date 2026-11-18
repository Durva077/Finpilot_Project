
import { useState } from 'react'
import { User, Mail, Phone, MapPin, Save } from 'lucide-react'

function Profile() {
  const [profile, setProfile] = useState({
    name: 'Sunidhi',
    email: 'sunidhi@example.com',
    phone: '',
    location: 'Goa, India',
  })

  const [saved, setSaved] = useState(false)

  function handleChange(event) {
    setProfile({ ...profile, [event.target.name]: event.target.value })
    setSaved(false)
  }

  function handleSubmit(event) {
    event.preventDefault()
    setSaved(true)
  }

  return (
    <div className="page-content">
      <header className="page-header">
        <div>
          <p className="eyebrow">YOUR ACCOUNT</p>
          <h1>My Profile</h1>
          <p className="subtitle">Manage your personal information.</p>
        </div>
      </header>

      <section className="profile-card">
        <div className="profile-banner">
          <div className="profile-avatar">
            {profile.name.charAt(0).toUpperCase() || 'U'}
          </div>
          <div>
            <h2>{profile.name || 'Your Name'}</h2>
            <p>{profile.email}</p>
          </div>
        </div>

        <form className="profile-form" onSubmit={handleSubmit}>
          <h2>Personal Information</h2>

          <label>Full Name</label>
          <div className="profile-input">
            <User size={18} />
            <input name="name" value={profile.name} onChange={handleChange} required />
          </div>

          <label>Email Address</label>
          <div className="profile-input">
            <Mail size={18} />
            <input name="email" type="email" value={profile.email} onChange={handleChange} required />
          </div>

          <label>Phone Number</label>
          <div className="profile-input">
            <Phone size={18} />
            <input name="phone" value={profile.phone} onChange={handleChange} placeholder="Enter phone number" />
          </div>

          <label>Location</label>
          <div className="profile-input">
            <MapPin size={18} />
            <input name="location" value={profile.location} onChange={handleChange} />
          </div>

          <button className="add-button" type="submit">
            <Save size={17} /> Save Changes
          </button>

          {saved && <p className="success-message">Profile changes saved for this session.</p>}
        </form>
      </section>
    </div>
  )
}

export default Profile
