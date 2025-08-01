import React, { useEffect, useState } from 'react'
import Layout from '../components/Layout'
import { DocumentTextIcon, XCircleIcon } from '@heroicons/react/24/outline'

interface Mop {
  id: string
  title: string
  category: string
  region: string
  variables_file: string
}

export default function Home() {
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

  if (loading) {
    return (
      <Layout title="Dashboard - MOP Ansible Renderer">
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
        </div>
      </Layout>
    )
  }

  if (error) {
    return (
      <Layout title="Dashboard - MOP Ansible Renderer">
        <div className="text-center py-12">
          <XCircleIcon className="mx-auto h-12 w-12 text-red-500 mb-4" />
          <h2 className="text-xl font-semibold text-white mb-2">Error Loading Dashboard</h2>
          <p className="text-gray-400 mb-4">{error}</p>
          <button onClick={fetchMops} className="btn btn-primary">
            Retry
          </button>
        </div>
      </Layout>
    )
  }

  return (
    <Layout title="Dashboard - MOP Ansible Renderer">
      <div className="px-4 sm:px-0">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">
            MOP Automation Dashboard
          </h1>
          <p className="text-gray-400">
            Manage and execute operational procedures with automated workflows
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="card">
            <div className="card-body text-center">
              <DocumentTextIcon className="h-8 w-8 text-blue-500 mx-auto mb-2" />
              <div className="text-2xl font-bold text-white">{mops.length}</div>
              <div className="text-sm text-gray-400">Available MOPs</div>
            </div>
          </div>
        </div>

        <div className="mb-6">
          <h2 className="text-xl font-bold text-white mb-4">Available MOPs</h2>
          
          {mops.length > 0 ? (
            <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
              {mops.map((mop) => (
                <div key={mop.id} className="card hover:shadow-xl transition-shadow duration-200">
                  <div className="card-header">
                    <h3 className="text-lg font-semibold text-white">{mop.title}</h3>
                  </div>
                  <div className="card-body">
                    <div className="space-y-2 mb-4">
                      <div className="text-sm text-gray-400">
                        <span className="font-mono">{mop.id}</span>
                      </div>
                      <div className="text-sm text-gray-400">
                        <span>{mop.region}</span>
                      </div>
                      <div>
                        <span className="badge badge-primary">{mop.category}</span>
                      </div>
                    </div>
                    
                    <div className="flex justify-end">
                      <a
                        href={`http://localhost:5000/mops/${mop.id}`}
                        className="btn btn-primary text-sm"
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
              <div className="card-body text-center py-12">
                <DocumentTextIcon className="h-12 w-12 text-gray-500 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-white mb-2">No MOPs Found</h3>
                <p className="text-gray-400 mb-4">
                  Get started by adding YAML variable files to the vars/ directory.
                </p>
                <a href="http://localhost:5000" className="btn btn-primary">
                  Go to Admin Panel
                </a>
              </div>
            </div>
          )}
        </div>
      </div>
    </Layout>
  )
}