// Client Component Example
// Uses 'use client' directive for interactivity

'use client'

import { useState, useEffect } from 'react'

interface LikeButtonProps {
  postId: string
  initialLikes: number
}

export function LikeButton({ postId, initialLikes }: LikeButtonProps) {
  const [likes, setLikes] = useState(initialLikes)
  const [isLiked, setIsLiked] = useState(false)
  const [isLoading, setIsLoading] = useState(false)

  // Check if user has liked this post (from localStorage)
  useEffect(() => {
    const likedPosts = JSON.parse(localStorage.getItem('likedPosts') || '[]')
    setIsLiked(likedPosts.includes(postId))
  }, [postId])

  const handleLike = async () => {
    setIsLoading(true)

    try {
      const newLikedState = !isLiked

      // Optimistic update
      setIsLiked(newLikedState)
      setLikes(newLikedState ? likes + 1 : likes - 1)

      // Update localStorage
      const likedPosts = JSON.parse(localStorage.getItem('likedPosts') || '[]')
      if (newLikedState) {
        likedPosts.push(postId)
      } else {
        const index = likedPosts.indexOf(postId)
        if (index > -1) likedPosts.splice(index, 1)
      }
      localStorage.setItem('likedPosts', JSON.stringify(likedPosts))

      // Send to API
      await fetch('/api/like', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ postId, liked: newLikedState }),
      })
    } catch (error) {
      // Revert on error
      setIsLiked(!isLiked)
      setLikes(isLiked ? likes + 1 : likes - 1)
      console.error('Failed to update like:', error)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <button
      onClick={handleLike}
      disabled={isLoading}
      className={`px-4 py-2 rounded-lg transition-colors ${
        isLiked
          ? 'bg-red-500 text-white hover:bg-red-600'
          : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
      } disabled:opacity-50`}
    >
      {isLiked ? '❤️' : '🤍'} {likes}
    </button>
  )
}
