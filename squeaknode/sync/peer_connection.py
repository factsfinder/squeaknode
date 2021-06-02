import logging
from contextlib import contextmanager
from typing import Optional

from squeaknode.core.block_range import BlockRange
from squeaknode.core.peer_address import PeerAddress
from squeaknode.core.received_offer_with_peer import ReceivedOfferWithPeer
from squeaknode.network.peer_client import PeerClient
from squeaknode.node.squeak_controller import SqueakController
from squeaknode.sync.download_criteria import DownloadCriteria
from squeaknode.sync.download_criteria import HashCriteria
from squeaknode.sync.download_criteria import RangeCriteria

logger = logging.getLogger(__name__)


class PeerConnection:

    def __init__(
        self,
        squeak_controller: SqueakController,
        peer_address: PeerAddress,
        timeout_s,
    ):
        self.squeak_controller = squeak_controller
        self.peer_address = peer_address
        self.timeout_s = timeout_s
        self.peer_client = PeerClient(
            self.peer_address.host,
            self.peer_address.port,
            self.timeout_s,
        )

    @contextmanager
    def open_connection(self):
        with self.peer_client.open_stub():
            yield self

    def download(
        self,
        block_range: BlockRange = None,
    ):
        # Get the network
        network = self.squeak_controller.get_network()
        # Get the block range
        if block_range is None:
            block_range = self.squeak_controller.get_block_range()
        # Get list of followed addresses
        followed_addresses = self.squeak_controller.get_followed_addresses()
        # Get remote hashes
        lookup_result = self.peer_client.lookup_squeaks_to_download(
            network,
            followed_addresses,
            block_range.min_block,
            block_range.max_block,
        )
        remote_hashes = lookup_result.hashes
        # Download squeaks and offers
        criteria = RangeCriteria(
            block_range=block_range,
            follow_list=followed_addresses,
        )
        for squeak_hash in remote_hashes:
            self._download_squeak(squeak_hash, criteria)

    def upload(self):
        # Get the network
        network = self.squeak_controller.get_network()
        # Get list of sharing addresses.
        sharing_addresses = self.squeak_controller.get_sharing_addresses()
        # Get remote hashes
        lookup_result = self.peer_client.lookup_squeaks_to_upload(
            network,
            sharing_addresses,
        )
        remote_hashes = lookup_result.hashes
        remote_addresses = lookup_result.addresses
        min_block = lookup_result.min_block
        max_block = lookup_result.max_block
        # Get local hashes
        local_hashes = self.squeak_controller.lookup_squeaks(
            remote_addresses,
            min_block,
            max_block,
        )
        # Get hashes to upload
        hashes_to_upload = set(local_hashes) - set(remote_hashes)
        # Upload squeaks for the hashes
        # TODO: catch exception uploading individual squeak
        for hash in hashes_to_upload:
            self._upload_squeak(hash)

    def download_single_squeak(self, squeak_hash: bytes):
        """Downloads a single squeak and the corresponding offer. """
        logger.info("Downloading single squeak {} from peer with address: {}".format(
            squeak_hash.hex(), self.peer_address
        ))
        criteria = HashCriteria(
            squeak_hash=squeak_hash,
        )
        self._download_squeak(squeak_hash, criteria)

    def _download_squeak(self, squeak_hash: bytes, criteria: DownloadCriteria):
        """Downloads a single squeak and the corresponding offer. """
        saved_squeak = self.squeak_controller.get_squeak(squeak_hash)
        if not saved_squeak:
            self._download_squeak_object(squeak_hash, criteria)
        saved_offer = self._get_saved_offer(squeak_hash)
        if not saved_offer:
            self._download_offer(squeak_hash, criteria)

    def upload_single_squeak(self, squeak_hash: bytes):
        """Uploads a single squeak. """
        local_squeak = self.squeak_controller.get_squeak(squeak_hash)
        if local_squeak and local_squeak.HasDecryptionKey():
            self._upload_squeak(squeak_hash)

    def _get_saved_offer(self, squeak_hash: bytes) -> Optional[ReceivedOfferWithPeer]:
        return self.squeak_controller.get_received_offer_for_squeak_and_peer(
            squeak_hash,
            self.peer_address,
        )

    def _download_squeak_object(self, squeak_hash: bytes, criteria: DownloadCriteria):
        squeak = self.peer_client.download_squeak(squeak_hash)
        if criteria.is_interested(squeak):
            self._save_squeak(squeak)

    def _save_squeak(self, squeak):
        self.squeak_controller.save_downloaded_squeak(
            squeak,
        )

    def _download_offer(self, squeak_hash: bytes, criteria: DownloadCriteria):
        squeak = self.squeak_controller.get_squeak(squeak_hash)
        offer = self.peer_client.download_offer(squeak_hash)
        decoded_offer = self.squeak_controller.get_offer(
            squeak,
            offer,
            self.peer_address,
        )
        if criteria.is_interested(squeak):
            self.squeak_controller.save_offer(decoded_offer)
        logger.info("Downloaded offer for squeak {} from peer with address: {}".format(
            squeak_hash.hex(), self.peer_address
        ))

    def _upload_squeak(self, squeak_hash: bytes):
        squeak = self.squeak_controller.get_squeak(squeak_hash)
        self.peer_client.upload_squeak(squeak)
        logger.info("Uploaded squeak {} to peer with address: {}".format(
            squeak_hash.hex(), self.peer_address
        ))
