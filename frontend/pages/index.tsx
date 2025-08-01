import { useEffect, useState } from 'react'
import Layout from '@/components/Layout'
import MopCard from '@/components/MopCard'
import { ClockIcon, DocumentTextIcon, CheckCircleIcon, XCircleIcon } from '@heroicons/react/24/outline'

interface Mop {
  id: string
  title: string
  category: string
  region: string
  variables_file: string
}

interface RecentExecution {
  mop_id: string
  timestamp: string
  success: boolean
  execution_id: string
}

export default function Home() {
  const [mops, setMops] = useState<Mop[]>([])
  const [recentExecutions, setRecentExecutions] = useState<RecentExecution[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      setLoading(true)
      
      // Fetch MOPs
      const mopsResponse = await fetch('/api/mops')
      if (!mopsResponse.ok) {
        throw new Error('Failed to fetch MOPs')
      }
      const mopsData = await mopsResponse.json()
      
      if (mopsData.success) {
        setMops(mopsData.mops)
      } else {
        throw new Error(mopsData.error || 'Failed to load MOPs')
      }

      // For recent executions, we'll simulate some data since the API doesn't provide this endpoint
      // In a real implementation, you'd fetch from /api/executions/recent
      setRecentExecutions([])
      
    } catch (err) {
      console.error('Error fetching data:', err)
      setError(err instanceof Error ? err.message : 'Failed to load data')
    } finally {
      setLoading(false)
    }
  }

  const successfulExecutions = recentExecutions.filter(exec => exec.success).length
  const failedExecutions = recentExecutions.length - successfulExecutions
  const categories = [...new Set(mops.map(mop => mop.category))]

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
          <button
            onClick={fetchData}
            className="btn btn-primary"
          >
            Retry
          </button>
        </div>
      </Layout>
    )
  }

  return (
    <Layout title="Dashboard - MOP Ansible Renderer">
      <div className="px-4 sm:px-0">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">
            MOP Automation Dashboard
          </h1>
          <p className="text-gray-400">
            Manage and execute operational procedures with automated workflows
          </p>
        </div>

        {/* Stats Overview */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="card">
            <div className="card-body text-center">
              <DocumentTextIcon className="h-8 w-8 text-blue-500 mx-auto mb-2" />
              <div className="text-2xl font-bold text-white">{mops.length}</div>
              <div className="text-sm text-gray-400">Available MOPs</div>
            </div>
          </div>
          
          <div className="card">
            <div className="card-body text-center">
              <ClockIcon className="h-8 w-8 text-purple-500 mx-auto mb-2" />
              <div className="text-2xl font-bold text-white">{recentExecutions.length}</div>
              <div className="text-sm text-gray-400">Recent Executions</div>
            </div>
          </div>
          
          <div className="card">
            <div className="card-body text-center">
              <CheckCircleIcon className="h-8 w-8 text-green-500 mx-auto mb-2" />
              <div className="text-2xl font-bold text-white">{successfulExecutions}</div>
              <div className="text-sm text-gray-400">Successful</div>
            </div>
          </div>
          
          <div className="card">
            <div className="card-body text-center">
              <XCircleIcon className="h-8 w-8 text-red-500 mx-auto mb-2" />
              <div className="text-2xl font-bold text-white">{failedExecutions}</div>
              <div className="text-sm text-gray-400">Failed</div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* MOPs List */}
          <div className="lg:col-span-2">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-xl font-bold text-white">Available MOPs</h2>
              <button
                onClick={fetchData}
                className="btn btn-secondary text-sm"
              >
                Refresh
              </button>
            </div>
            
            {mops.length > 0 ? (
              <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
                {mops.map((mop) => (
                  <MopCard key={mop.id} mop={mop} />
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
                  <a href="/admin" className="btn btn-primary">
                    Go to Admin Panel
                  </a>
                </div>
              </div>
            )}
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Categories */}
            <div className="card">
              <div className="card-header">
                <h3 className="text-lg font-semibold text-white">Categories</h3>
              </div>
              <div className="card-body">
                {categories.length > 0 ? (
                  <div className="space-y-2">
                    {categories.map((category) => {
                      const count = mops.filter(mop => mop.category === category).length
                      return (
                        <div key={category} className="flex justify-between items-center">
                          <span className="text-gray-300">{category}</span>
                          <span className="badge badge-primary">{count}</span>
                        </div>
                      )
                    })}
                  </div>
                ) : (
                  <p className="text-gray-400 text-sm">No categories available</p>
                )}
              </div>
            </div>

            {/* Quick Actions */}
            <div className="card">
              <div className="card-header">
                <h3 className="text-lg font-semibold text-white">Quick Actions</h3>
              </div>
              <div className="card-body space-y-3">
                <a href="/admin" className="btn btn-primary w-full text-center block">
                  Admin Panel
                </a>
                <button 
                  onClick={fetchData}
                  className="btn btn-secondary w-full"
                >
                  Refresh Data
                </button>
              </div>
            </div>

            {/* Recent Activity */}
            {recentExecutions.length > 0 && (
              <div className="card">
                <div className="card-header">
                  <h3 className="text-lg font-semibold text-white">Recent Activity</h3>
                </div>
                <div className="card-body">
                  <div className="space-y-3">
                    {recentExecutions.slice(0, 5).map((execution) => (
                      <div key={execution.execution_id} className="flex items-center justify-between">
                        <div>
                          <div className="text-sm font-medium text-white">{execution.mop_id}</div>
                          <div className="text-xs text-gray-400">
                            {new Date(execution.timestamp).toLocaleDateString()}
                          </div>
                        </div>
                        <span className={`badge ${execution.success ? 'badge-success' : 'badge-danger'}`}>
                          {execution.success ? 'Success' : 'Failed'}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </Layout>
  )
}