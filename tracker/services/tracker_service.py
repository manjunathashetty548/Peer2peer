from tracker.models.schemas import (
    RegisterPeerRequest,
    RegisterPeerResponse,
    PeerInfo,
    PeersListResponse,
    FilePeersResponse,
    HealthResponse,
)
from tracker.storage.memory_store import TrackerStore, store


class TrackerService:
    """
    Business logic layer for tracker operations.
    Acts as an intermediary between controller routes and state storage.
    """

    def __init__(self, data_store: TrackerStore = store) -> None:
        self.store = data_store

    def register_peer(self, request: RegisterPeerRequest) -> RegisterPeerResponse:
        """Processes registration for a new or existing peer."""
        peer_info = PeerInfo(
            peer_id=request.peer_id,
            host=request.host,
            port=request.port,
            files=request.files,
        )
        files_count = self.store.register_peer(peer_info)
        return RegisterPeerResponse(
            status="success",
            message=f"Peer '{request.peer_id}' registered successfully.",
            peer_id=request.peer_id,
            registered_files_count=files_count,
        )

    def list_peers(self) -> PeersListResponse:
        """Retrieves all registered peers."""
        peers = self.store.get_all_peers()
        return PeersListResponse(
            total_peers=len(peers),
            peers=peers,
        )

    def get_peers_for_file(self, filename: str) -> FilePeersResponse:
        """Finds peers hosting a given filename."""
        peers = self.store.get_peers_for_file(filename)
        return FilePeersResponse(
            filename=filename,
            peer_count=len(peers),
            peers=peers,
        )

    def check_health(self) -> HealthResponse:
        """Returns tracker status metrics."""
        active_peers, tracked_files = self.store.get_stats()
        return HealthResponse(
            status="ok",
            active_peers=active_peers,
            tracked_files_count=tracked_files,
        )
