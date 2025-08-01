import { useEffect } from 'react'
import { useRouter } from 'next/router'
import Layout from '@/components/Layout'
import { ExternalLinkIcon } from '@heroicons/react/24/outline'

export default function AdminRedirect() {
  const router = useRouter()

  useEffect(() => {
    // Redirect to Flask admin interface
    window.location.href = 'http://localhost:5000'
  }, [])

  return (
    <Layout title="Redirecting to Admin Panel...">
      <div className="text-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
        <h2 className="text-xl font-semibold text-white mb-2">Redirecting to Admin Panel</h2>
        <p className="text-gray-400 mb-4">
          You will be redirected to the Flask admin interface...
        </p>
        <a 
          href="http://localhost:5000"
          className="btn btn-primary inline-flex items-center"
        >
          <ExternalLinkIcon className="h-4 w-4 mr-2" />
          Go to Admin Panel
        </a>
      </div>
    </Layout>
  )
}