# MIT License
#
# Copyright (c) 2020 Jonathan Zernik
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import logging
import threading
from concurrent import futures

import grpc

from proto import squeak_admin_pb2
from proto import squeak_admin_pb2_grpc

logger = logging.getLogger(__name__)


class SqueakAdminServerServicer(squeak_admin_pb2_grpc.SqueakAdminServicer):
    """Provides methods that implement functionality of squeak admin server."""

    def __init__(self, host, port, handler):
        self.host = host
        self.port = port
        self.handler = handler
        self.server = None

    def start(self):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=100))
        squeak_admin_pb2_grpc.add_SqueakAdminServicer_to_server(
            self, self.server)
        self.server.add_insecure_port("{}:{}".format(self.host, self.port))
        logger.info("Starting SqueakAdminServerServicer...")
        self.server.start()

    def stop(self):
        if self.server is None:
            return
        self.server.stop(None)
        logger.info("Stopped SqueakAdminServerServicer.")

    def LndGetInfo(self, request, context):
        return self.handler.handle_lnd_get_info(request)

    def LndWalletBalance(self, request, context):
        return self.handler.handle_lnd_wallet_balance(request)

    def LndNewAddress(self, request, context):
        return self.handler.handle_lnd_new_address(request)

    def LndListChannels(self, request, context):
        return self.handler.handle_lnd_list_channels(request)

    def LndPendingChannels(self, request, context):
        return self.handler.handle_lnd_pending_channels(request)

    def LndGetTransactions(self, request, context):
        return self.handler.handle_lnd_get_transactions(request)

    def LndListPeers(self, request, context):
        return self.handler.handle_lnd_list_peers(request)

    def LndConnectPeer(self, request, context):
        return self.handler.handle_lnd_connect_peer(request)

    def LndDisconnectPeer(self, request, context):
        return self.handler.handle_lnd_disconnect_peer(request)

    def LndOpenChannelSync(self, request, context):
        return self.handler.handle_lnd_open_channel_sync(request)

    def LndCloseChannel(self, request, context):
        return self.handler.handle_lnd_close_channel(request)

    def LndSubscribeChannelEvents(self, request, context):
        return self.handler.handle_lnd_subscribe_channel_events(request)

    def LndSendCoins(self, request, context):
        return self.handler.handle_lnd_send_coins(request)

    def CreateSigningProfile(self, request, context):
        return self.handler.handle_create_signing_profile(request)

    def ImportSigningProfile(self, request, context):
        return self.handler.handle_import_signing_profile(request)

    def CreateContactProfile(self, request, context):
        return self.handler.handle_create_contact_profile(request)

    def GetProfiles(self, request, context):
        return self.handler.handle_get_profiles(request)

    def GetSigningProfiles(self, request, context):
        return self.handler.handle_get_signing_profiles(request)

    def GetContactProfiles(self, request, context):
        return self.handler.handle_get_contact_profiles(request)

    def GetSqueakProfile(self, request, context):
        reply = self.handler.handle_get_squeak_profile(request)
        if reply is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Profile not found.")
            return squeak_admin_pb2.GetSqueakProfileReply()
        return reply

    def GetSqueakProfileByAddress(self, request, context):
        return self.handler.handle_get_squeak_profile_by_address(request)

    def GetSqueakProfileByName(self, request, context):
        return self.handler.handle_get_squeak_profile_by_name(request)

    def SetSqueakProfileFollowing(self, request, context):
        return self.handler.handle_set_squeak_profile_following(request)

    def SetSqueakProfileUseCustomPrice(self, request, context):
        return self.handler.handle_set_squeak_profile_use_custom_price(request)

    def SetSqueakProfileCustomPrice(self, request, context):
        return self.handler.handle_set_squeak_profile_custom_price(request)

    def RenameSqueakProfile(self, request, context):
        return self.handler.handle_rename_squeak_profile(request)

    def DeleteSqueakProfile(self, request, context):
        return self.handler.handle_delete_squeak_profile(request)

    def SetSqueakProfileImage(self, request, context):
        return self.handler.handle_set_squeak_profile_image(request)

    def ClearSqueakProfileImage(self, request, context):
        return self.handler.handle_clear_squeak_profile_image(request)

    def GetSqueakProfilePrivateKey(self, request, context):
        return self.handler.handle_get_squeak_profile_private_key(request)

    def MakeSqueak(self, request, context):
        return self.handler.handle_make_squeak(request)

    def GetSqueakDisplay(self, request, context):
        return self.handler.handle_get_squeak_display_entry(request)

    def GetTimelineSqueakDisplays(self, request, context):
        return self.handler.handle_get_timeline_squeak_display_entries(request)

    def GetAddressSqueakDisplays(self, request, context):
        return self.handler.handle_get_squeak_display_entries_for_address(request)

    def GetAncestorSqueakDisplays(self, request, context):
        return self.handler.handle_get_ancestor_squeak_display_entries(request)

    def GetReplySqueakDisplays(self, request, context):
        return self.handler.handle_get_reply_squeak_display_entries(request)

    def DeleteSqueak(self, request, context):
        return self.handler.handle_delete_squeak(request)

    def CreatePeer(self, request, context):
        return self.handler.handle_create_peer(request)

    def GetPeer(self, request, context):
        reply = self.handler.handle_get_squeak_peer(request)
        if reply is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Peer not found.")
            return squeak_admin_pb2.GetPeerReply()
        return reply

    def GetPeers(self, request, context):
        return self.handler.handle_get_squeak_peers(request)

    def SetPeerAutoconnect(self, request, context):
        return self.handler.handle_set_squeak_peer_autoconnect(request)

    def RenamePeer(self, request, context):
        return self.handler.handle_rename_squeak_peer(request)

    def DeletePeer(self, request, context):
        return self.handler.handle_delete_squeak_peer(request)

    def GetBuyOffers(self, request, context):
        return self.handler.handle_get_buy_offers(request)

    def GetBuyOffer(self, request, context):
        return self.handler.handle_get_buy_offer(request)

    def DownloadSqueaks(self, request, context):
        return self.handler.handle_download_squeaks(request)

    def DownloadSqueak(self, request, context):
        return self.handler.handle_download_squeak(request)

    def DownloadOffers(self, request, context):
        return self.handler.handle_download_offers(request)

    def DownloadReplies(self, request, context):
        return self.handler.handle_download_replies(request)

    def DownloadAddressSqueaks(self, request, context):
        return self.handler.handle_download_address_squeaks(request)

    def PayOffer(self, request, context):
        return self.handler.handle_pay_offer(request)

    def GetSentPayments(self, request, context):
        return self.handler.handle_get_sent_payments(request)

    def GetSentPayment(self, request, context):
        return self.handler.handle_get_sent_payment(request)

    def GetSqueakDetails(self, request, context):
        return self.handler.handle_get_squeak_details(request)

    def GetSentOffers(self, request, context):
        return self.handler.handle_get_sent_offers(request)

    def GetReceivedPayments(self, request, context):
        return self.handler.handle_get_received_payments(request)

    def SubscribeReceivedPayments(self, request, context):
        stopped = threading.Event()

        def on_rpc_done():
            logger.info("Stopping SubscribeReceivedPayments.")
            stopped.set()
        context.add_callback(on_rpc_done)
        return self.handler.handle_subscribe_received_payments(
            request,
            stopped,
        )

    def GetNetwork(self, request, context):
        return self.handler.handle_get_network(request)

    def GetPaymentSummary(self, request, context):
        return self.handler.handle_get_payment_summary(request)

    def ReprocessReceivedPayments(self, request, context):
        return self.handler.handle_reprocess_received_payments(request)

    def LikeSqueak(self, request, context):
        return self.handler.handle_like_squeak(request)

    def UnlikeSqueak(self, request, context):
        return self.handler.handle_unlike_squeak(request)

    def GetLikedSqueakDisplays(self, request, context):
        return self.handler.handle_get_liked_squeak_display_entries(request)

    def ConnectPeer(self, request, context):
        return self.handler.handle_connect_peer(request)

    def GetConnectedPeers(self, request, context):
        return self.handler.handle_get_connected_peers(request)

    def GetConnectedPeer(self, request, context):
        return self.handler.handle_get_connected_peer(request)

    def DisconnectPeer(self, request, context):
        return self.handler.handle_disconnect_peer(request)

    def SubscribeConnectedPeers(self, request, context):
        stopped = threading.Event()

        def on_rpc_done():
            logger.info("Stopping SubscribeConnectedPeers.")
            stopped.set()
        context.add_callback(on_rpc_done)
        return self.handler.handle_subscribe_connected_peers(
            request,
            stopped,
        )

    def SubscribeConnectedPeer(self, request, context):
        stopped = threading.Event()

        def on_rpc_done():
            logger.info("Stopping SubscribeConnectedPeer.")
            stopped.set()
        context.add_callback(on_rpc_done)
        return self.handler.handle_subscribe_connected_peer(
            request,
            stopped,
        )

    def SubscribeBuyOffers(self, request, context):
        stopped = threading.Event()

        def on_rpc_done():
            logger.info("Stopping SubscribeBuyOffers.")
            stopped.set()
        context.add_callback(on_rpc_done)
        return self.handler.handle_subscribe_buy_offers(
            request,
            stopped,
        )

    def SubscribeSqueakDisplay(self, request, context):
        stopped = threading.Event()

        def on_rpc_done():
            logger.info("Stopping SubscribeSqueakDisplay.")
            stopped.set()
        context.add_callback(on_rpc_done)
        return self.handler.handle_subscribe_squeak_display(
            request,
            stopped,
        )

    def SubscribeReplySqueakDisplays(self, request, context):
        stopped = threading.Event()

        def on_rpc_done():
            logger.info("Stopping SubscribeReplySqueakDisplays.")
            stopped.set()
        context.add_callback(on_rpc_done)
        return self.handler.handle_subscribe_reply_squeak_displays(
            request,
            stopped,
        )

    def SubscribeAddressSqueakDisplays(self, request, context):
        stopped = threading.Event()

        def on_rpc_done():
            logger.info("Stopping SubscribeAddressSqueakDisplaysRequest.")
            stopped.set()
        context.add_callback(on_rpc_done)
        return self.handler.handle_subscribe_address_squeak_displays(
            request,
            stopped,
        )

    def SubscribeAncestorSqueakDisplays(self, request, context):
        stopped = threading.Event()

        def on_rpc_done():
            logger.info("Stopping SubscribeAncestorSqueakDisplays.")
            stopped.set()
        context.add_callback(on_rpc_done)
        return self.handler.handle_subscribe_ancestor_squeak_displays(
            request,
            stopped,
        )

    def SubscribeSqueakDisplays(self, request, context):
        stopped = threading.Event()

        def on_rpc_done():
            logger.info("Stopping SubscribeSqueakDisplays.")
            stopped.set()
        context.add_callback(on_rpc_done)
        return self.handler.handle_subscribe_squeak_displays(
            request,
            stopped,
        )

    def SubscribeTimelineSqueakDisplays(self, request, context):
        stopped = threading.Event()

        def on_rpc_done():
            logger.info("Stopping SubscribeTimelineSqueakDisplays.")
            stopped.set()
        context.add_callback(on_rpc_done)
        return self.handler.handle_subscribe_timeline_squeak_displays(
            request,
            stopped,
        )

    def GetExternalAddress(self, request, context):
        return self.handler.handle_get_external_address(request)
