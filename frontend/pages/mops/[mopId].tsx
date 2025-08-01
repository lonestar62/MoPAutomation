import { useRouter } from 'next/router'
import { useEffect, useState } from 'react'
import Layout from '@/components/Layout'
import ExecutionLog from '@/components/ExecutionLog'
import ReactMarkdown from 'react-markdown'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { vscDarkPlus } from 'react-syntax-highlighter/dist/cjs/styles/prism'
import { 
  PlayIcon, 
  PencilIcon, 
  ArrowLeftIcon,
  ClockIcon,
  TagIcon,
  MapPinIcon,
  DocumentTextIcon 
} from '@heroicons/react/24/outline'

interface MopData {
  id: string
  variables: Record<string, any>
  template: string
  frontmatter: Record<string, any>
  content: string
  rendered_content: string
  playbooks: string[]
}

interface ExecutionHistory {
  execution_id: string
  mop_id: string
  timestamp: string
  category: string
  playbooks: string[]
  success: boolean
  results: any[]
  variables: Record<string, any>
  error?: string
}

export default function MopDetail() {
  const router = useRouter()
  const { mopId } = router.query
  
  const [mop, setMop] = useState<MopData | null>(null)
  const [history, setHistory] = useState<ExecutionHistory[]>([])
  const [loading, setLoading] = useState(true)
  const [executing, setExecuting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (mopId && typeof mopId === 'string') {
      fetchMopData(mopId)
    }
  }, [mopId])

  const fetchMopData = async (id: string) => {
    try {
      setLoading(true)
      setError(null)

      // Fetch MOP details
      const mopResponse = await fetch(`/api/mops/${id}`)
      if (!mopResponse.ok) {
        throw new Error('Failed to fetch MOP details')
      }
      const mopData = await mopResponse.json()
      
      if (mopData.success) {
        setMop(mopData.mop)
      } else {
        throw new Error(mopData.error || 'Failed to load MOP')
      }

      // For execution history, we'll simulate since we don't have a specific endpoint
      // In a real implementation, you'd fetch from /api/mops/${id}/history
      setHistory([])
      
    } catch (err) {
      console.error('Error fetching MOP data:', err)
      setError(err instanceof Error ? err.message : 'Failed to load MOP')
    } finally {
      setLoading(false)
    }
  }

  const executeMop = async () => {
    if (!mopId || typeof mopId !== 'string') return

    try {
      setExecuting(true)
      
      const response = await fetch(`/api/mops/${mopId}/execute`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      })
      
      if (!response.ok) {
        throw new Error('Failed to execute MOP')
      }
      
      const result = await response.json()
      
      if (result.success) {
        // Refresh the page data to show new execution
        await fetchMopData(mopId)
        
        // Show success message
        alert('MOP executed successfully!')
      } else {
        throw new Error(result.error || 'MOP execution failed')
      }
      
    } catch (err) {
      console.error('Error executing MOP:', err)
      alert(err instanceof Error ? err.message : 'Failed to execute MOP')
    } finally {
      setExecuting(false)
    }
  }

  if (loading) {
    return (
      <Layout title="Loading MOP...">
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
        </div>
      </Layout>
    )
  }

  if (error || !mop) {
    return (
      <Layout title="MOP Not Found">
        <div className="text-center py-12">
          <DocumentTextIcon className="mx-auto h-12 w-12 text-red-500 mb-4" />
          <h2 className="text-xl font-semibold text-white mb-2">MOP Not Found</h2>
          <p className="text-gray-400 mb-4">{error || 'The requested MOP could not be found.'}</p>
          <button
            onClick={() => router.back()}
            className="btn btn-secondary"
          >
            <ArrowLeftIcon className="h-4 w-4 mr-2" />
            Go Back
          </button>
        </div>
      </Layout>
    )
  }

  return (
    <Layout title={`${mop.variables.title} - MOP Details`}>
      <div className="px-4 sm:px-0">
        {/* Breadcrumb */}
        <nav className="flex mb-6" aria-label="Breadcrumb">
          <ol className="inline-flex items-center space-x-1 md:space-x-3">
            <li>
              <button
                onClick={() => router.push('/')}
                className="text-gray-400 hover:text-white"
              >
                Dashboard
              </button>
            </li>
            <li>
              <div className="flex items-center">
                <span className="text-gray-500 mx-2">/</span>
                <span className="text-white">{mop.id}</span>
              </div>
            </li>
          </ol>
        </nav>

        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-white mb-2">{mop.variables.title}</h1>
            <p className="text-gray-400 font-mono">{mop.id}</p>
          </div>
          <div className="flex space-x-3 mt-4 sm:mt-0">
            <button
              onClick={executeMop}
              disabled={executing}
              className="btn btn-success flex items-center"
            >
              <PlayIcon className="h-4 w-4 mr-2" />
              {executing ? 'Executing...' : 'Execute MOP'}
            </button>
            <a
              href={`/admin/vars/${mop.id}/edit`}
              className="btn btn-secondary flex items-center"
            >
              <PencilIcon className="h-4 w-4 mr-2" />
              Edit Variables
            </a>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* Rendered MOP Content */}
            <div className="card">
              <div className="card-header">
                <h2 className="text-lg font-semibold text-white">Rendered MOP Content</h2>
              </div>
              <div className="card-body">
                <div className="markdown-content">
                  <ReactMarkdown
                    components={{
                      code({node, inline, className, children, ...props}) {
                        const match = /language-(\w+)/.exec(className || '')
                        return !inline && match ? (
                          <SyntaxHighlighter
                            style={vscDarkPlus}
                            language={match[1]}
                            PreTag="div"
                            {...props}
                          >
                            {String(children).replace(/\n$/, '')}
                          </SyntaxHighlighter>
                        ) : (
                          <code className={className} {...props}>
                            {children}
                          </code>
                        )
                      }
                    }}
                  >
                    {mop.content}
                  </ReactMarkdown>
                </div>
              </div>
            </div>

            {/* Execution History */}
            <div>
              <h2 className="text-lg font-semibold text-white mb-4">Execution History</h2>
              {history.length > 0 ? (
                <div className="space-y-4">
                  {history.map((execution) => (
                    <ExecutionLog key={execution.execution_id} execution={execution} />
                  ))}
                </div>
              ) : (
                <div className="card">
                  <div className="card-body text-center py-8">
                    <ClockIcon className="h-12 w-12 text-gray-500 mx-auto mb-4" />
                    <h3 className="text-lg font-medium text-white mb-2">No Execution History</h3>
                    <p className="text-gray-400">Execute this MOP to see history here</p>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* MOP Metadata */}
            <div className="card">
              <div className="card-header">
                <h3 className="text-lg font-semibold text-white">MOP Metadata</h3>
              </div>
              <div className="card-body">
                <dl className="space-y-3">
                  <div>
                    <dt className="text-sm text-gray-400 flex items-center">
                      <TagIcon className="h-4 w-4 mr-1" />
                      ID
                    </dt>
                    <dd className="font-mono text-white">{mop.id}</dd>
                  </div>
                  
                  <div>
                    <dt className="text-sm text-gray-400">Title</dt>
                    <dd className="text-white">{mop.variables.title}</dd>
                  </div>
                  
                  <div>
                    <dt className="text-sm text-gray-400">Category</dt>
                    <dd>
                      <span className="badge badge-primary">{mop.variables.category}</span>
                    </dd>
                  </div>
                  
                  <div>
                    <dt className="text-sm text-gray-400 flex items-center">
                      <MapPinIcon className="h-4 w-4 mr-1" />
                      Region
                    </dt>
                    <dd className="text-white">{mop.variables.region}</dd>
                  </div>
                  
                  <div>
                    <dt className="text-sm text-gray-400">Template</dt>
                    <dd className="font-mono text-white text-sm">{mop.template}</dd>
                  </div>
                </dl>
              </div>
            </div>

            {/* Associated Playbooks */}
            <div className="card">
              <div className="card-header">
                <h3 className="text-lg font-semibold text-white">Associated Playbooks</h3>
              </div>
              <div className="card-body">
                {mop.playbooks && mop.playbooks.length > 0 ? (
                  <div className="space-y-2">
                    {mop.playbooks.map((playbook) => (
                      <div key={playbook} className="flex items-center justify-between">
                        <span className="font-mono text-white text-sm">{playbook}</span>
                        <span className="badge badge-secondary text-xs">Ansible</span>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-gray-400 text-sm">No playbooks associated with this category.</p>
                )}
              </div>
            </div>

            {/* Variables */}
            <div className="card">
              <div className="card-header">
                <h3 className="text-lg font-semibold text-white">Variables</h3>
              </div>
              <div className="card-body">
                <div className="code-block">
                  <pre className="text-sm">
                    {JSON.stringify(mop.variables, null, 2)}
                  </pre>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  )
}