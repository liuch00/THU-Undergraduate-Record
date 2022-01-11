#include "checksum.h"
#include <assert.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

/* Compute Internet Checksum for "count" bytes
*         beginning at location "addr".
*  The implementation of this function refers to rfc1071;
*/
uint16_t checkSum(uint8_t *addr, int count)
{
  long sum = 0;
  uint16_t checksum = 0;
  while (count > 1)
  {
    /*  This is the inner loop */
    sum += *(unsigned short *)addr++;
    addr++;
    count -= 2;
  }
  /*  Add left-over byte, if any */
  if (count > 0)
    sum += *(unsigned char *)addr;

  /*  Fold 32-bit sum to 16 bits */
  while (sum >> 16)
    sum = (sum & 0xffff) + (sum >> 16);

  checksum = ~sum;
  return checksum;
}

bool validateAndFillChecksum(uint8_t *packet, size_t len)
{
  // TODO
  struct ip6_hdr *ip6 = (struct ip6_hdr *)packet;

  // check next header
  uint16_t get_checksum;
  uint16_t correct_checksum;

  uint8_t nxt_header = ip6->ip6_nxt;
  if (nxt_header == IPPROTO_UDP)
  {
    // UDP
    struct udphdr *udp = (struct udphdr *)&packet[sizeof(struct ip6_hdr)];
    // length: udp->uh_ulen
    // checksum: udp->uh_sum
    get_checksum = udp->uh_sum;
    correct_checksum;
    udp->uh_sum = 0;
    int hs = ntohs(udp->uh_ulen);
    int count = 40 + hs;
    uint8_t *IPv6_pseudo_header = new uint8_t[count];
    memset(IPv6_pseudo_header, 0, count);
    memcpy(IPv6_pseudo_header, (uint8_t *)ip6->ip6_src.s6_addr, 32);
    memcpy(IPv6_pseudo_header + 34, &udp->uh_ulen, 2);
    IPv6_pseudo_header[39] = nxt_header;
    memcpy(IPv6_pseudo_header + 40, udp, hs);
    correct_checksum = checkSum(IPv6_pseudo_header, count);
    delete[] IPv6_pseudo_header;
  }
  else if (nxt_header == IPPROTO_ICMPV6)
  {
    // ICMPv6
    struct icmp6_hdr *icmp =
        (struct icmp6_hdr *)&packet[sizeof(struct ip6_hdr)];
    // length: len-sizeof(struct ip6_hdr)
    // checksum: icmp->icmp6_cksum
    get_checksum = icmp->icmp6_cksum;
    correct_checksum;
    icmp->icmp6_cksum = 0;
    int hs = ntohs(ip6->ip6_plen);
    int count = 40 + hs;
    uint8_t *IPv6_pseudo_header = new uint8_t[count];
    memset(IPv6_pseudo_header, 0, count);
    memcpy(IPv6_pseudo_header, (uint8_t *)ip6->ip6_src.s6_addr, 32);
    memcpy(IPv6_pseudo_header + 34, &ip6->ip6_plen, 2);
    IPv6_pseudo_header[39] = nxt_header;
    memcpy(IPv6_pseudo_header + 40, icmp, hs);
    correct_checksum = checkSum(IPv6_pseudo_header, count);
    delete[] IPv6_pseudo_header;
    //check and update
    // icmp->icmp6_cksum = correct_checksum;
    // if ((get_checksum == 0xffff && correct_checksum == 0x0000) || get_checksum == correct_checksum)
    // {
    //   return true;
    // }
    // else
    // {
    //   return false;
    // }
  }
  else
  {
    assert(false);
  }
  if (nxt_header == IPPROTO_UDP) {
    // UDP
    struct udphdr *udp = (struct udphdr *)&packet[sizeof(struct ip6_hdr)];
  
    if (correct_checksum == 0x0000)
    {
      udp->uh_sum = 0xffff;
    }
    else
    {
      udp->uh_sum = correct_checksum;
    }
    if (get_checksum == 0x0000)
    {
      return false;
    }
    if (get_checksum != correct_checksum&&(get_checksum!=0xffff||correct_checksum))
    {
      return false;
    }
    return true;
  }
  else if (nxt_header==IPPROTO_ICMPV6){
    // ICMPv6
    struct icmp6_hdr *icmp =
        (struct icmp6_hdr *)&packet[sizeof(struct ip6_hdr)];
    icmp->icmp6_cksum=correct_checksum;
    if (get_checksum==correct_checksum)
    {
      return true;
    }
    if (get_checksum!=0xffff||correct_checksum)
    {
      return false;
    }
    return true;
  }

  return (get_checksum==0xffff && correct_checksum==0x0000 || correct_checksum == get_checksum)?true:false;
 
}
