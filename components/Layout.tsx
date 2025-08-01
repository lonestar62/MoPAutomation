import React, { ReactNode } from 'react'
import Head from 'next/head'
import Link from 'next/link'
import { CogIcon, DocumentTextIcon, HomeIcon } from '@heroicons/react/24/outline'

interface LayoutProps {
  children: ReactNode
  title?: string
}

export default function Layout({ children, title = 'MOP Ansible Renderer' }: LayoutProps) {
  return (
    <div className="min-h-screen bg-gray-900">
      <Head>
        <title>{title}</title>
        <meta name="description" content="MOP-Driven Ansible Automation Platform" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      {/* Navigation */}
      <nav className="bg-gray-800 border-b border-gray-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <Link href="/" className="flex items-center space-x-2 text-white font-bold text-xl">
                <CogIcon className="h-8 w-8 text-blue-500" />
                <span>MOP Renderer</span>
              </Link>
              
              <div className="hidden md:block ml-10">
                <div className="flex items-baseline space-x-4">
                  <Link
                    href="/"
                    className="text-gray-300 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium flex items-center space-x-1"
                  >
                    <HomeIcon className="h-4 w-4" />
                    <span>Dashboard</span>
                  </Link>
                  <Link
                    href="/admin"
                    className="text-gray-300 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium flex items-center space-x-1"
                  >
                    <DocumentTextIcon className="h-4 w-4" />
                    <span>Admin Panel</span>
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        {children}
      </main>

      {/* Footer */}
      <footer className="bg-gray-800 border-t border-gray-700 mt-12">
        <div className="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center">
            <p className="text-gray-400 text-sm">
              MOP-Driven Ansible Automation Platform
            </p>
            <p className="text-gray-400 text-sm">
              Built with Flask & Next.js
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}