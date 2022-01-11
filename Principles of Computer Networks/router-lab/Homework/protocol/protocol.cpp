#include "protocol.h"
#include "common.h"
#include "lookup.h"
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

RipErrorCode disassemble(const uint8_t *packet, uint32_t len,
                         RipPacket *output)
{
  //  1. len 是否包括一个的 IPv6 header 的长度。
  if (len < sizeof(ip6_hdr))
  {
    return RipErrorCode::ERR_LENGTH;
  }
  //  2. IPv6 Header 中的 Payload Length 加上 Header 长度是否等于 len。
  struct ip6_hdr *ip6 = (struct ip6_hdr *)packet;
  if (sizeof(ip6_hdr) + ntohs(ip6->ip6_plen) != len)
  {
    return RipErrorCode::ERR_LENGTH;
  }
  //  3. IPv6 Header 中的 Next header 字段是否为 UDP 协议。
  if (ip6->ip6_nxt != IPPROTO_UDP)
  {
    return RipErrorCode::ERR_IP_NEXT_HEADER_NOT_UDP;
  }
  //  4. IPv6 Header 中的 Payload Length 是否包括一个 UDP header 的长度。
  if (ntohs(ip6->ip6_plen) < sizeof(udphdr))
  {
    return RipErrorCode::ERR_LENGTH;
  }

  //  5. 检查 UDP 源端口和目的端口是否都为 521。
  struct udphdr *udp = (struct udphdr *)&packet[sizeof(struct ip6_hdr)];
  int sport = ntohs(udp->uh_sport);
  int dport = ntohs(udp->uh_dport);
  if (sport != 521 || dport != 521)
  {
    return RipErrorCode::ERR_BAD_UDP_PORT;
  }
  //  6. 检查 UDP header 中 Length 是否等于 UDP header 长度加上 RIPng header 长度加上 RIPng entry 长度的整数倍。
  if ((ntohs(udp->uh_ulen) - sizeof(udphdr) - sizeof(ripng_hdr)) % sizeof(ripng_entry))
  {
    return RipErrorCode::ERR_LENGTH;
  }

  //  7. 检查 RIPng header 中的 Command 是否为 1 或 2， Version 是否为 1，Zero（Reserved） 是否为 0。
  ripng_hdr *riphdr = (struct ripng_hdr *)&packet[sizeof(struct ip6_hdr) + sizeof(udphdr)];
  if ((riphdr->command != 1) && (riphdr->command != 2))
  {
    return RipErrorCode::ERR_RIP_BAD_COMMAND;
  }
  if (riphdr->version != 1)
  {
    return RipErrorCode::ERR_RIP_BAD_VERSION;
  }
  if (riphdr->zero != 0)
  {
    return RipErrorCode::ERR_RIP_BAD_ZERO;
  }

  //  8. 对每个 RIPng entry，当 Metric=0xFF 时，检查 Prefix Len 和 Route Tag 是否为 0。
  //  9. 对每个 RIPng entry，当 Metric!=0xFF 时，检查 Metric 是否属于 [1,16]，并检查 Prefix Len 是否属于 [0,128]，是否与 IPv6 prefix 字段组成合法的 IPv6 前缀。
  uint32_t numEntries = (ntohs(udp->uh_ulen) - sizeof(udphdr) - sizeof(ripng_hdr)) / sizeof(ripng_entry);
  


  for (int i = 0; i < numEntries; i++)
  {
    ripng_entry *entry = (ripng_entry *)&packet[sizeof(struct ip6_hdr) + sizeof(udphdr) + sizeof(ripng_hdr) + sizeof(ripng_entry) * i];
    if (entry->metric == 0xFF)
    {
      if (entry->route_tag != 0)
      {
        return RipErrorCode::ERR_RIP_BAD_ROUTE_TAG;
      }
      if (entry->prefix_len != 0)
      {
        return RipErrorCode::ERR_RIP_BAD_PREFIX_LEN;
      }
    }
    else
    {
      if (entry->metric > 16 || entry->metric < 1)
      {
        return RipErrorCode::ERR_RIP_BAD_METRIC;
      }
      if (entry->prefix_len > 128 || entry->prefix_len < 0)
      {
        return RipErrorCode::ERR_RIP_BAD_PREFIX_LEN;
      }
      //是否与 IPv6 prefix 字段组成合法的 IPv6 前缀
      if((len_to_mask(entry->prefix_len) & entry->prefix_or_nh) != entry->prefix_or_nh ||
          mask_to_len(len_to_mask(entry->prefix_len)) != entry->prefix_len){
          return RipErrorCode::ERR_RIP_INCONSISTENT_PREFIX_LENGTH;
      }
    }
  }
  output->command = riphdr->command;
  output->numEntries = numEntries;
  for (int i = 0; i < numEntries; i++){
    ripng_entry *entry = (ripng_entry *)&packet[sizeof(struct ip6_hdr) + sizeof(udphdr) + sizeof(ripng_hdr) + sizeof(ripng_entry) * i];
    output->entries[i].prefix_or_nh= entry->prefix_or_nh;
    output->entries[i].route_tag= entry->route_tag;
    output->entries[i].prefix_len=entry->prefix_len;
    output->entries[i].metric=entry->metric;
  }

  return RipErrorCode::SUCCESS;
}



uint32_t assemble(const RipPacket *rip, uint8_t *buffer)
{
  // TODO
  buffer[0]=rip->command;
  buffer[1]=1;
  buffer[2]=0;
  buffer[3]=0;

  memcpy(buffer+4,rip->entries, sizeof(ripng_entry)*rip->numEntries);
  return 4 + 20 * rip->numEntries;
}