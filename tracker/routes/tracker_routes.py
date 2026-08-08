from fastapi import APIRouter, Depends, status
from tracker.models.schemas import (
    RegisterPeerRequest,
    RegisterPeerResponse,
    PeersListResponse,
    FilePeersResponse,
    HealthResponse,
)
from tracker.services.tracker_service import TrackerService

router = APIRouter(tags=["Tracker Core"])


def get_tracker_service() -> TrackerService:
    """Dependency provider for TrackerService."""
    return TrackerService()


@router.post(
    "/register",
    response_model=RegisterPeerResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register Peer",
    description="Registers a peer server's metadata (IP, port) and the list of files it hosts.",
)
def register_peer(
    request: RegisterPeerRequest,
    service: TrackerService = Depends(get_tracker_service),
) -> RegisterPeerResponse:
    return service.register_peer(request)


@router.get(
    "/peers",
    response_model=PeersListResponse,
    status_code=status.HTTP_200_OK,
    summary="List All Peers",
    description="Returns a list of all currently registered peers in the P2P network.",
)
def list_peers(
    service: TrackerService = Depends(get_tracker_service),
) -> PeersListResponse:
    return service.list_peers()


@router.get(
    "/peers/{filename}",
    response_model=FilePeersResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Peers For File",
    description="Returns all active peers that possess the specified filename.",
)
def get_peers_for_file(
    filename: str,
    service: TrackerService = Depends(get_tracker_service),
) -> FilePeersResponse:
    return service.get_peers_for_file(filename)


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Tracker Health Check",
    description="Returns current operational status of the tracker server along with active peer statistics.",
)
def health_check(
    service: TrackerService = Depends(get_tracker_service),
) -> HealthResponse:
    return service.check_health()
