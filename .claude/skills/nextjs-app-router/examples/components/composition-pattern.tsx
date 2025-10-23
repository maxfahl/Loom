// Composition Pattern: Server Components inside Client Components
// Pass Server Components as children/props to Client Components

'use client'

import { useState } from 'react'

// Client Component that provides interactivity
export function Modal({ children }: { children: React.ReactNode }) {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <>
      <button
        onClick={() => setIsOpen(true)}
        className="px-4 py-2 bg-blue-500 text-white rounded"
      >
        Open Modal
      </button>

      {isOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
          <div className="bg-white p-6 rounded-lg max-w-2xl max-h-[80vh] overflow-auto">
            <button
              onClick={() => setIsOpen(false)}
              className="float-right text-gray-500 hover:text-gray-700"
            >
              ✕
            </button>
            {/* Children can be Server Components! */}
            {children}
          </div>
        </div>
      )}
    </>
  )
}

// Usage in a Server Component parent:

// app/page.tsx (Server Component)
import { Modal } from './components/modal'
import { UserProfile } from './components/user-profile' // Server Component

export default async function Page() {
  return (
    <div>
      <h1>Welcome</h1>
      <Modal>
        {/* UserProfile is a Server Component that fetches data */}
        <UserProfile userId="123" />
      </Modal>
    </div>
  )
}
