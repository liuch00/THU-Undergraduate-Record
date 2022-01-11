#include "lookup.h"
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <map>

const uint8_t LEN_TO_MASK_8[9] = {
    0,
    0x80,
    0xc0,
    0xe0,
    0xf0,
    0xf8,
    0xfc,
    0xfe,
    0xff,
};

using LEN_ADDR_PAIR = std::pair<uint32_t, in6_addr>;
std::map<LEN_ADDR_PAIR, RoutingTableEntry> RT;

void update(bool insert, const RoutingTableEntry entry)
{
  LEN_ADDR_PAIR la_pair = {entry.len, entry.addr};
  if (insert)
  {
    RT[la_pair] = entry;
  }
  else
  {
    auto iter = RT.find(la_pair);
    if (iter != RT.end())
      RT.erase(iter);
  }
}

bool prefix_query(const in6_addr addr, in6_addr *nexthop, uint32_t *if_index)
{
  for (int i = 128; i >= 0; --i)
  {
    in6_addr maskedAddr = addr & len_to_mask(i);
    auto iter = RT.find(LEN_ADDR_PAIR(i, maskedAddr));
    if (iter != RT.end())
    {
      *if_index = iter->second.if_index;
      *nexthop = iter->second.nexthop;
      return true;
    }
  }
  return false;
}

int mask_to_len(const in6_addr mask)
{
  int len = 0;
  for (int i = 0; i < 16; i++)
  {
    for (int j = 1; j < 9; j++)
    {
      if (mask.s6_addr[i] == LEN_TO_MASK_8[j])
      {
        len += j;
        break;
      }
    }
  }
  return len;
}

in6_addr len_to_mask(int len)
{
  in6_addr mask;
  for (int i = 0; i < 16; i++)
  {
    mask.s6_addr[i] = 0;
  }
  int quotient = len / 8;
  int remainder = len % 8;
  for (int i = 0; i < quotient; i++)
  {
    mask.s6_addr[i] = LEN_TO_MASK_8[8];
  }
  if (quotient != 16)
  {
    for (int i = 1; i < 9; i++)
    {
      if (remainder == i)
      {
        mask.s6_addr[quotient] = LEN_TO_MASK_8[i];
        break;
      }
    }
  }
  return mask;
}
