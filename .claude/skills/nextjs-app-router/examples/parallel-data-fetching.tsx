/**
 * Parallel Data Fetching Example
 *
 * This example demonstrates how to fetch multiple data sources in parallel
 * to avoid request waterfalls and improve performance.
 */

// ✅ GOOD: Parallel fetching with Promise.all
export default async function ArtistPage({ params }: { params: { id: string } }) {
  // Define fetch functions
  async function getArtist(id: string) {
    const res = await fetch(`https://api.example.com/artists/${id}`);
    if (!res.ok) throw new Error('Failed to fetch artist');
    return res.json();
  }

  async function getAlbums(id: string) {
    const res = await fetch(`https://api.example.com/artists/${id}/albums`);
    if (!res.ok) throw new Error('Failed to fetch albums');
    return res.json();
  }

  async function getTopTracks(id: string) {
    const res = await fetch(`https://api.example.com/artists/${id}/tracks`);
    if (!res.ok) throw new Error('Failed to fetch tracks');
    return res.json();
  }

  // Initiate all requests in parallel
  const artistPromise = getArtist(params.id);
  const albumsPromise = getAlbums(params.id);
  const tracksPromise = getTopTracks(params.id);

  // Wait for all to complete
  const [artist, albums, tracks] = await Promise.all([
    artistPromise,
    albumsPromise,
    tracksPromise,
  ]);

  return (
    <div className="artist-page">
      <header>
        <img src={artist.image} alt={artist.name} />
        <h1>{artist.name}</h1>
        <p>{artist.bio}</p>
      </header>

      <section>
        <h2>Albums</h2>
        <div className="albums-grid">
          {albums.map((album: any) => (
            <div key={album.id}>{album.title}</div>
          ))}
        </div>
      </section>

      <section>
        <h2>Top Tracks</h2>
        <ul>
          {tracks.map((track: any) => (
            <li key={track.id}>{track.name}</li>
          ))}
        </ul>
      </section>
    </div>
  );
}

// ❌ BAD: Sequential fetching creates waterfall
async function BadSequentialExample({ params }: { params: { id: string } }) {
  // Each request waits for the previous one to complete
  const artist = await fetch(`/api/artists/${params.id}`).then(r => r.json());
  const albums = await fetch(`/api/artists/${params.id}/albums`).then(r => r.json());
  const tracks = await fetch(`/api/artists/${params.id}/tracks`).then(r => r.json());

  // This could take 3x longer than parallel fetching!
  return <div>...</div>;
}

// ✅ GOOD: Parallel fetching with streaming
import { Suspense } from 'react';

async function Artist({ id }: { id: string }) {
  const res = await fetch(`https://api.example.com/artists/${id}`);
  const artist = await res.json();
  return (
    <header>
      <h1>{artist.name}</h1>
      <p>{artist.bio}</p>
    </header>
  );
}

async function Albums({ artistId }: { artistId: string }) {
  const res = await fetch(`https://api.example.com/artists/${artistId}/albums`);
  const albums = await res.json();
  return (
    <div className="albums-grid">
      {albums.map((album: any) => (
        <div key={album.id}>{album.title}</div>
      ))}
    </div>
  );
}

async function TopTracks({ artistId }: { artistId: string }) {
  const res = await fetch(`https://api.example.com/artists/${artistId}/tracks`);
  const tracks = await res.json();
  return (
    <ul>
      {tracks.map((track: any) => (
        <li key={track.id}>{track.name}</li>
      ))}
    </ul>
  );
}

export function StreamingArtistPage({ params }: { params: { id: string } }) {
  return (
    <div className="artist-page">
      <Suspense fallback={<div>Loading artist info...</div>}>
        <Artist id={params.id} />
      </Suspense>

      <Suspense fallback={<div>Loading albums...</div>}>
        <Albums artistId={params.id} />
      </Suspense>

      <Suspense fallback={<div>Loading tracks...</div>}>
        <TopTracks artistId={params.id} />
      </Suspense>
    </div>
  );
}

// ✅ GOOD: Using React cache for deduplication
import { cache } from 'react';

const getUser = cache(async (id: string) => {
  const res = await fetch(`https://api.example.com/users/${id}`);
  return res.json();
});

// Multiple components can call getUser with same ID - only one request is made
async function UserProfile({ userId }: { userId: string }) {
  const user = await getUser(userId);
  return <div>{user.name}</div>;
}

async function UserSettings({ userId }: { userId: string }) {
  const user = await getUser(userId); // Reuses cached result
  return <div>{user.email}</div>;
}

// ✅ GOOD: Preload pattern for dependent data
const preloadUser = (id: string) => {
  void getUser(id); // Start fetching without awaiting
};

const preloadPosts = (userId: string) => {
  void cache(async () => {
    const res = await fetch(`https://api.example.com/users/${userId}/posts`);
    return res.json();
  })();
};

export async function UserDashboard({ params }: { params: { id: string } }) {
  // Start preloading data
  preloadUser(params.id);
  preloadPosts(params.id);

  // Do other work here
  const isAdmin = await checkAdminStatus();

  // Data is already loading in the background
  const user = await getUser(params.id);

  return <div>...</div>;
}

// ✅ GOOD: Handling parallel requests with error boundaries
export async function RobustParallelFetch({ params }: { params: { id: string } }) {
  const [artistResult, albumsResult, tracksResult] = await Promise.allSettled([
    getArtist(params.id),
    getAlbums(params.id),
    getTopTracks(params.id),
  ]);

  const artist = artistResult.status === 'fulfilled' ? artistResult.value : null;
  const albums = albumsResult.status === 'fulfilled' ? albumsResult.value : [];
  const tracks = tracksResult.status === 'fulfilled' ? tracksResult.value : [];

  return (
    <div>
      {artist ? (
        <header>
          <h1>{artist.name}</h1>
        </header>
      ) : (
        <div>Failed to load artist info</div>
      )}

      {albums.length > 0 ? (
        <section>Albums: {albums.length}</section>
      ) : (
        <div>No albums available</div>
      )}

      {tracks.length > 0 ? (
        <section>Tracks: {tracks.length}</section>
      ) : (
        <div>No tracks available</div>
      )}
    </div>
  );
}
