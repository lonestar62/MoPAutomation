import React, { useEffect, useState } from 'react'
import Head from 'next/head'

interface Mop {
  id: string
  title: string
  category: string
  region: string
  variables_file: string
}

export default function SimplePage() {
  const [mops, setMops] = useState<Mop[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchMops()
  }, [])

  const fetchMops = async () => {
    try {
      setLoading(true)
      setError(null)
      
      const response = await fetch('/api/mops')
      if (!response.ok) {
        throw new Error('Failed to fetch MOPs')
      }
      
      const data = await response.json()
      if (data.success) {
        setMops(data.mops)
      } else {
        throw new Error(data.error || 'Failed to load MOPs')
      }
    } catch (err) {
      console.error('Error fetching MOPs:', err)
      setError(err instanceof Error ? err.message : 'Failed to load data')
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      <Head>
        <title>MOP Ansible Renderer - Dashboard</title>
        <meta name="description" content="MOP-Driven Ansible Automation Platform" />
      </Head>

      <nav className="nav">
        <div className="nav-content">
          <a href="/" className="nav-brand">
            <span>🔧</span>
            MOP Renderer
          </a>
          <div>
            <a href="http://localhost:5000" className="btn btn-primary">
              Admin Panel
            </a>
          </div>
        </div>
      </nav>

      <div className="container">
        <div className="mb-4">
          <h1>MOP Automation Dashboard</h1>
          <p className="text-gray">
            Manage and execute operational procedures with automated workflows
          </p>
        </div>

        {loading && (
          <div className="loading">
            <div className="spinner"></div>
          </div>
        )}

        {error && (
          <div className="card">
            <div className="card-body text-center">
              <h2>Error Loading Dashboard</h2>
              <p className="text-gray mb-4">{error}</p>
              <button onClick={fetchMops} className="btn btn-primary">
                Retry
              </button>
            </div>
          </div>
        )}

        {!loading && !error && (
          <>
            <div className="card mb-4">
              <div className="card-body text-center">
                <h2>{mops.length}</h2>
                <p className="text-gray">Available MOPs</p>
              </div>
            </div>

            <div className="mb-4">
              <h2>Available MOPs</h2>
              
              {mops.length > 0 ? (
                <div className="grid grid-cols-1">
                  {mops.map((mop) => (
                    <div key={mop.id} className="card">
                      <div className="card-header">
                        <h3>{mop.title}</h3>
                      </div>
                      <div className="card-body">
                        <p className="text-gray mb-2">ID: {mop.id}</p>
                        <p className="text-gray mb-2">Region: {mop.region}</p>
                        <div className="mb-4">
                          <span className="badge">{mop.category}</span>
                        </div>
                        
                        <div style={{ textAlign: 'right' }}>
                          <a
                            href={`http://localhost:5000/mops/${mop.id}`}
                            className="btn btn-primary"
                            target="_blank"
                            rel="noopener noreferrer"
                          >
                            View Details
                          </a>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="card">
                  <div className="card-body text-center">
                    <h3>No MOPs Found</h3>
                    <p className="text-gray mb-4">
                      Get started by adding YAML variable files to the vars/ directory.
                    </p>
                    <a href="http://localhost:5000" className="btn btn-primary">
                      Go to Admin Panel
                    </a>
                  </div>
                </div>
              )}
            </div>
          </>
        )}
      </div>
    </>
  )
}