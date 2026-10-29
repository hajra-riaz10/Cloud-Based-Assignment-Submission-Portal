
import { useEffect, useState } from 'react';
import api from '../services/api';

const emptyForm = {
  student_name: '',
  registration_number: '',
  assignment_title: '',
  submission_url: '',
};

export default function PublicSubmissionPage() {
  const [form, setForm] = useState(emptyForm);
  const [submissions, setSubmissions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  async function loadSubmissions() {
    try {
      const response = await api.get('/url-submissions/');
      setSubmissions(response.data);
    } catch {
      setError('Could not load submissions. Please check that the backend is running.');
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadSubmissions();
  }, []);

  function handleChange(event) {
    setForm({ ...form, [event.target.name]: event.target.value });
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setMessage('');
    setError('');
    setSaving(true);

    try {
      await api.post('/url-submissions/', {
        student_name: form.student_name.trim(),
        registration_number: form.registration_number.trim(),
        assignment_title: form.assignment_title.trim(),
        submission_url: form.submission_url.trim(),
      });

      setMessage('Submission saved successfully!');
      setForm(emptyForm);
      await loadSubmissions();
    } catch (err) {
      const detail = err.response?.data?.detail;
      setError(
        typeof detail === 'string'
          ? detail
          : 'Submission failed. Please check your details and URL.'
      );
    } finally {
      setSaving(false);
    }
  }

  return (
    <main style={styles.page}>
      <section style={styles.container}>
        <header style={styles.header}>
          <h1 style={styles.heading}>Assignment Submission Portal</h1>
          <p style={styles.subtitle}>
            Enter your details and submit your assignment link.
          </p>
        </header>

        <form onSubmit={handleSubmit} style={styles.form}>
          <label style={styles.label}>
            Student Name
            <input
              style={styles.input}
              name="student_name"
              value={form.student_name}
              onChange={handleChange}
              placeholder="Enter your full name"
              maxLength={150}
              required
            />
          </label>

          <label style={styles.label}>
            Registration Number
            <input
              style={styles.input}
              name="registration_number"
              value={form.registration_number}
              onChange={handleChange}
              placeholder="e.g. FA22-BCS-001"
              maxLength={50}
              required
            />
          </label>

          <label style={styles.label}>
            Assignment Title
            <input
              style={styles.input}
              name="assignment_title"
              value={form.assignment_title}
              onChange={handleChange}
              placeholder="Enter assignment title"
              maxLength={200}
              required
            />
          </label>

          <label style={styles.label}>
            Submission URL
            <input
              style={styles.input}
              type="url"
              name="submission_url"
              value={form.submission_url}
              onChange={handleChange}
              placeholder="https://github.com/username/project"
              maxLength={2048}
              required
            />
          </label>

          {message && <p role="status" style={styles.success}>{message}</p>}
          {error && <p role="alert" style={styles.error}>{error}</p>}

          <button type="submit" disabled={saving} style={styles.button}>
            {saving ? 'Submitting...' : 'Submit Assignment'}
          </button>
        </form>

        <section style={styles.listSection}>
          <h2 style={styles.listHeading}>Saved Submissions</h2>

          {loading ? (
            <p>Loading submissions...</p>
          ) : submissions.length === 0 ? (
            <p>No submissions yet.</p>
          ) : (
            <div style={styles.tableWrapper}>
              <table style={styles.table}>
                <thead>
                  <tr>
                    <th style={styles.cell}>Student</th>
                    <th style={styles.cell}>Assignment</th>
                    <th style={styles.cell}>Submission Link</th>
                  </tr>
                </thead>
                <tbody>
                  {submissions.map((item) => (
                    <tr key={item.id}>
                      <td style={styles.cell}>{item.student_name}</td>
                      <td style={styles.cell}>{item.assignment_title}</td>
                      <td style={styles.cell}>
                        <a
                          href={item.submission_url}
                          target="_blank"
                          rel="noreferrer"
                          style={styles.link}
                        >
                          Open Link
                        </a>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>
      </section>
    </main>
  );
}

const styles = {
  page: {
    minHeight: '100vh',
    background: '#f4f6fc',
    padding: '36px 16px',
    fontFamily: 'Arial, sans-serif',
    color: '#172554',
  },
  container: {
    maxWidth: '850px',
    margin: '0 auto',
    background: '#ffffff',
    padding: '30px',
    borderRadius: '12px',
    boxShadow: '0 4px 20px rgba(30, 41, 59, 0.08)',
  },
  header: { textAlign: 'center', marginBottom: '28px' },
  heading: { fontSize: '28px', marginBottom: '10px', color: '#1e3a8a' },
  subtitle: { color: '#64748b', margin: 0 },
  form: { display: 'grid', gap: '16px' },
  label: { display: 'grid', gap: '7px', fontWeight: 600, fontSize: '14px' },
  input: {
    boxSizing: 'border-box',
    width: '100%',
    padding: '12px',
    border: '1px solid #cbd5e1',
    borderRadius: '6px',
    fontSize: '15px',
  },
  button: {
    padding: '13px',
    background: '#1e40af',
    color: '#ffffff',
    border: 'none',
    borderRadius: '6px',
    fontSize: '16px',
    fontWeight: 600,
    cursor: 'pointer',
  },
  success: { color: '#166534', background: '#dcfce7', padding: '10px' },
  error: { color: '#b91c1c', background: '#fee2e2', padding: '10px' },
  listSection: { marginTop: '36px' },
  listHeading: { fontSize: '22px', color: '#1e3a8a' },
  tableWrapper: { overflowX: 'auto' },
  table: { width: '100%', borderCollapse: 'collapse', textAlign: 'left' },
  cell: {
    padding: '12px',
    border: '1px solid #e2e8f0',
    overflowWrap: 'anywhere',
  },
  link: { color: '#1d4ed8', fontWeight: 600 },
};
