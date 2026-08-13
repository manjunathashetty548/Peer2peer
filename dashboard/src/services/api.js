const TRACKER_BASE_URL = import.meta.env.VITE_TRACKER_URL || 'http://127.0.0.1:8000';

/**
 * Fetch operational health status and active peer/file statistics from Tracker.
 */
export async function fetchHealth() {
  try {
    const response = await fetch(`${TRACKER_BASE_URL}/health`);
    if (!response.ok) throw new Error(`HTTP error ${response.status}`);
    return await response.json();
  } catch (error) {
    console.error('Tracker API Health check failed:', error);
    return { status: 'offline', active_peers: 0, tracked_files_count: 0 };
  }
}

/**
 * Fetch list of all registered peers in the P2P network.
 */
export async function fetchPeers() {
  try {
    const response = await fetch(`${TRACKER_BASE_URL}/peers`);
    if (!response.ok) throw new Error(`HTTP error ${response.status}`);
    const data = await response.json();
    return data.peers || [];
  } catch (error) {
    console.error('Tracker API Fetch Peers failed:', error);
    return [];
  }
}

/**
 * Fetch all peers hosting a specific filename.
 */
export async function fetchFilePeers(filename) {
  try {
    const response = await fetch(`${TRACKER_BASE_URL}/peers/${encodeURIComponent(filename)}`);
    if (!response.ok) throw new Error(`HTTP error ${response.status}`);
    const data = await response.json();
    return data.peers || [];
  } catch (error) {
    console.error(`Tracker API Fetch File Peers for '${filename}' failed:`, error);
    return [];
  }
}
