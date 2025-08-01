import { useState } from 'react'
import { ChevronDownIcon, ChevronRightIcon } from '@heroicons/react/24/outline'

interface ExecutionResult {
  playbook: string
  success: boolean
  return_code: number
  output: string
  start_time: string
  end_time: string
  duration_seconds: number
  error?: string
}

interface ExecutionLogProps {
  execution: {
    execution_id: string
    mop_id: string
    timestamp: string
    category: string
    playbooks: string[]
    success: boolean
    results: ExecutionResult[]
    variables: Record<string, any>
    error?: string
  }
}

export default function ExecutionLog({ execution }: ExecutionLogProps) {
  const [isExpanded, setIsExpanded] = useState(false)
  const [expandedPlaybooks, setExpandedPlaybooks] = useState<Set<string>>(new Set())

  const togglePlaybook = (playbook: string) => {
    const newExpanded = new Set(expandedPlaybooks)
    if (newExpanded.has(playbook)) {
      newExpanded.delete(playbook)
    } else {
      newExpanded.add(playbook)
    }
    setExpandedPlaybooks(newExpanded)
  }

  const formatTimestamp = (timestamp: string) => {
    return new Date(timestamp).toLocaleString()
  }

  return (
    <div className="card mb-4">
      <div 
        className="card-header cursor-pointer flex items-center justify-between"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <div className="flex items-center space-x-3">
          {isExpanded ? (
            <ChevronDownIcon className="h-5 w-5 text-gray-400" />
          ) : (
            <ChevronRightIcon className="h-5 w-5 text-gray-400" />
          )}
          <div>
            <h4 className="text-lg font-medium text-white">{execution.execution_id}</h4>
            <p className="text-sm text-gray-400">{formatTimestamp(execution.timestamp)}</p>
          </div>
        </div>
        
        <span className={`badge ${execution.success ? 'badge-success' : 'badge-danger'}`}>
          {execution.success ? 'Success' : 'Failed'}
        </span>
      </div>

      {isExpanded && (
        <div className="card-body">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
            <div>
              <h5 className="font-medium text-white mb-2">Execution Details</h5>
              <dl className="space-y-1 text-sm">
                <div className="flex">
                  <dt className="text-gray-400 w-20">MOP ID:</dt>
                  <dd className="text-white font-mono">{execution.mop_id}</dd>
                </div>
                <div className="flex">
                  <dt className="text-gray-400 w-20">Category:</dt>
                  <dd className="text-white">{execution.category}</dd>
                </div>
                <div className="flex">
                  <dt className="text-gray-400 w-20">Status:</dt>
                  <dd className="text-white">{execution.success ? 'Completed' : 'Failed'}</dd>
                </div>
              </dl>
            </div>
            
            <div>
              <h5 className="font-medium text-white mb-2">Playbooks</h5>
              <div className="space-y-1">
                {execution.playbooks.map((playbook) => (
                  <span key={playbook} className="badge badge-primary text-xs">
                    {playbook}
                  </span>
                ))}
              </div>
            </div>
          </div>

          {execution.error && (
            <div className="mb-6">
              <h5 className="font-medium text-red-400 mb-2">Error</h5>
              <div className="code-block">
                <pre className="text-red-300 text-sm">{execution.error}</pre>
              </div>
            </div>
          )}

          {execution.results && execution.results.length > 0 && (
            <div>
              <h5 className="font-medium text-white mb-3">Playbook Results</h5>
              <div className="space-y-3">
                {execution.results.map((result, index) => (
                  <div key={index} className="border border-gray-700 rounded-lg">
                    <div 
                      className="px-4 py-3 cursor-pointer flex items-center justify-between bg-gray-800 rounded-t-lg"
                      onClick={() => togglePlaybook(result.playbook)}
                    >
                      <div className="flex items-center space-x-3">
                        {expandedPlaybooks.has(result.playbook) ? (
                          <ChevronDownIcon className="h-4 w-4 text-gray-400" />
                        ) : (
                          <ChevronRightIcon className="h-4 w-4 text-gray-400" />
                        )}
                        <span className="font-medium text-white">{result.playbook}</span>
                      </div>
                      
                      <div className="flex items-center space-x-2">
                        <span className="text-sm text-gray-400">
                          {result.duration_seconds.toFixed(1)}s
                        </span>
                        <span className={`badge ${result.success ? 'badge-success' : 'badge-danger'}`}>
                          {result.success ? 'Success' : 'Failed'}
                        </span>
                      </div>
                    </div>

                    {expandedPlaybooks.has(result.playbook) && (
                      <div className="px-4 py-3 bg-gray-900">
                        <div className="grid grid-cols-2 gap-4 mb-4 text-sm">
                          <div>
                            <span className="text-gray-400">Start Time:</span>
                            <div className="text-white font-mono">
                              {formatTimestamp(result.start_time)}
                            </div>
                          </div>
                          <div>
                            <span className="text-gray-400">Return Code:</span>
                            <div className="text-white font-mono">{result.return_code}</div>
                          </div>
                        </div>

                        {result.error && (
                          <div className="mb-4">
                            <h6 className="text-red-400 font-medium mb-2">Error</h6>
                            <div className="code-block">
                              <pre className="text-red-300 text-sm">{result.error}</pre>
                            </div>
                          </div>
                        )}

                        <div>
                          <h6 className="text-gray-400 font-medium mb-2">Output</h6>
                          <div className="code-block">
                            <pre className="text-gray-300 text-sm whitespace-pre-wrap">
                              {result.output}
                            </pre>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}