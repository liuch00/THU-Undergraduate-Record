#include "checksum.h"
#include "common.h"
#include "eui64.h"
#include "lookup.h"
#include "protocol.h"
#include "router_hal.h"
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <map>

uint8_t packet[2048];
uint8_t output[2048];

// for online experiment, don't change
#ifdef ROUTER_R1
// 0: fd00::1:1/112
// 1: fd00::3:1/112
// 2: fd00::6:1/112
// 3: fd00::7:1/112
in6_addr addrs[N_IFACE_ON_BOARD] = {
    {0xfd, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
     0x00, 0x01, 0x00, 0x01},
    {0xfd, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
     0x00, 0x03, 0x00, 0x01},
    {0xfd, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
     0x00, 0x06, 0x00, 0x01},
    {0xfd, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
     0x00, 0x07, 0x00, 0x01},
};
#elif defined(ROUTER_R2)
// 0: fd00::3:2/112
// 1: fd00::4:1/112
// 2: fd00::8:1/112
// 3: fd00::9:1/112
in6_addr addrs[N_IFACE_ON_BOARD] = {
    {0xfd, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
     0x00, 0x03, 0x00, 0x02},
    {0xfd, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
     0x00, 0x04, 0x00, 0x01},
    {0xfd, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
     0x00, 0x08, 0x00, 0x01},
    {0xfd, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
     0x00, 0x09, 0x00, 0x01},
};
#elif defined(ROUTER_R3)
// 0: fd00::4:2/112
// 1: fd00::5:2/112
// 2: fd00::a:1/112
// 3: fd00::b:1/112
in6_addr addrs[N_IFACE_ON_BOARD] = {
    {0xfd, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
     0x00, 0x04, 0x00, 0x02},
    {0xfd, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
     0x00, 0x05, 0x00, 0x02},
    {0xfd, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
     0x00, 0x0a, 0x00, 0x01},
    {0xfd, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
     0x00, 0x0b, 0x00, 0x01},
};
#else

// 自己调试用，你可以按需进行修改
// 0: fd00::0:1
// 1: fd00::1:1
// 2: fd00::2:1
// 3: fd00::3:1
in6_addr addrs[N_IFACE_ON_BOARD] = {
    {0xfd, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
     0x00, 0x00, 0x00, 0x01},
    {0xfd, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
     0x00, 0x01, 0x00, 0x01},
    {0xfd, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
     0x00, 0x02, 0x00, 0x01},
    {0xfd, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
     0x00, 0x03, 0x00, 0x01},
};
#endif
using LEN_ADDR_PAIR = std::pair<uint32_t, in6_addr>;
extern std::map<LEN_ADDR_PAIR, RoutingTableEntry> RT;
void send_table(int if_index, in6_addr addr_src,in6_addr addr_dest,ether_addr mac){
  int cnt =0;
  RipPacket rip;
  for(auto item :RT){
    auto entry = item.second;
    rip.command =2;
    rip.entries[cnt].prefix_or_nh=entry.addr;
    rip.entries[cnt].route_tag=entry.route_tag;
    rip.entries[cnt].metric=entry.metric;
    rip.entries[cnt].prefix_len=entry.len;
    if(if_index==entry.if_index){
      rip.entries[cnt].metric=16;
    }
    cnt++;
    if(cnt>50){
      rip.numEntries = 50;  
      int hdr_len= sizeof(udphdr)+sizeof(ripng_hdr);
      int entrys_len= rip.numEntries *sizeof(ripng_entry);
      // IPv6 header
      ip6_hdr *ip6 = (ip6_hdr *)&output[0];
      // flow label
      ip6->ip6_flow = 0;
      // version
      ip6->ip6_vfc = 6 << 4;
      // payload length
      ip6->ip6_plen = htons(hdr_len+entrys_len);
      // next header
      ip6->ip6_nxt = IPPROTO_UDP;
      // hop limit
      ip6->ip6_hlim = 255;
      // src ip
      ip6->ip6_src = addr_src;
      // dst ip
      ip6->ip6_dst = addr_dest;

      udphdr *udp = (udphdr *)&output[sizeof(ip6_hdr)];
      // dst port
      udp->uh_dport = htons(521);
      // src port
      udp->uh_sport = htons(521);

      udp->uh_ulen =ip6->ip6_plen ;

      uint8_t *buffer=&output[48];
      RipPacket* s_rip=&rip;
      assemble(s_rip,buffer);

      validateAndFillChecksum(output,hdr_len+entrys_len+sizeof(ip6_hdr));
      HAL_SendIPPacket(if_index,output,hdr_len+entrys_len+sizeof(ip6_hdr),mac);
      if(RT.size() > 70){
        fprintf(stderr, "///////////////////////////////////\n");
        for(int i = 0; i < hdr_len+entrys_len+sizeof(ip6_hdr); i++){
          fprintf(stderr, "%02x", output[i]);
        }
        fprintf(stderr, "\n///////////////////////////////////\n");
      } 
      cnt =0;
    }
  }
  if(cnt>0){
   rip.numEntries = cnt;  
      int hdr_len= sizeof(udphdr)+sizeof(ripng_hdr);
      int entrys_len= rip.numEntries *sizeof(ripng_entry);
      // IPv6 header
      ip6_hdr *ip6 = (ip6_hdr *)&output[0];
      // flow label
      ip6->ip6_flow = 0;
      // version
      ip6->ip6_vfc = 6 << 4;
      // payload length
      ip6->ip6_plen = htons(hdr_len+entrys_len);
      // next header
      ip6->ip6_nxt = IPPROTO_UDP;
      // hop limit
      ip6->ip6_hlim = 255;
      // src ip
      ip6->ip6_src = addr_src;
      // dst ip
      ip6->ip6_dst = addr_dest;

      udphdr *udp = (udphdr *)&output[sizeof(ip6_hdr)];
      // dst port
      udp->uh_dport = htons(521);
      // src port
      udp->uh_sport = htons(521);

      udp->uh_ulen =ip6->ip6_plen ;

      uint8_t *buffer=&output[48];
      RipPacket* s_rip=&rip;
      assemble(s_rip,buffer);

      validateAndFillChecksum(output,hdr_len+entrys_len+sizeof(ip6_hdr));
      HAL_SendIPPacket(if_index,output,hdr_len+entrys_len+sizeof(ip6_hdr),mac);
      if(RT.size() > 70){
        fprintf(stderr, "///////////////////////////////////\n");
        for(int i = 0; i < hdr_len+entrys_len+sizeof(ip6_hdr); i++){
          fprintf(stderr, "%02x", output[i]);
        }
        fprintf(stderr, "\n///////////////////////////////////\n");
      } 
  }
}


int main(int argc, char *argv[]) {
  // 初始化 HAL
  int res = HAL_Init(1, addrs);
  if (res < 0) {
    return res;
  }

  // 插入直连路由
  // 例如 R2：
  // fd00::3:0/112 if 0
  // fd00::4:0/112 if 1
  // fd00::8:0/112 if 2
  // fd00::9:0/112 if 3
  for (uint32_t i = 0; i < N_IFACE_ON_BOARD; i++) {
    in6_addr mask = len_to_mask(112);
    RoutingTableEntry entry = {
        .addr = addrs[i] & mask,
        .len = 112,
        .if_index = i,
        .nexthop = in6_addr{0}, // 全 0 表示直连路由
        .route_tag=0,
        .metric=1
    };
    update(true, entry);
  }

  uint64_t last_time = 0;
  while (1) {
    uint64_t time = HAL_GetTicks();
    // RFC 要求每 30s 发送一次
    // 为了提高收敛速度，设为 5s
    if (time > last_time + 5 * 1000) {
      // 提示：你可以打印完整的路由表到 stdout/stderr 来帮助调试。
      printf("5s Timer\n");

      // 这一步需要向所有 interface 发送当前的完整路由表，设置 Command 为
      // Response，并且注意当路由表表项较多时，需要拆分为多个 IPv6 packet。此时
      // IPv6 packet 的源地址应为使用 eui64 计算得到的 Link Local
      // 地址，目的地址为 ff02::9，以太网帧的源 MAC 地址为当前 interface 的 MAC
      // 地址，目的 MAC 地址为 33:33:00:00:00:09，详见 RFC 2080 Section 2.5.2
      // Generating Response Messages。
      //
      // 注意需要实现水平分割以及毒性反转（Split Horizon with Poisoned Reverse）
      // 即，如果某一条路由表项是从 interface A 学习到的，那么发送给 interface A
      // 的 RIPng 表项中，该项的 metric 设为 16。详见 RFC 2080 Section 2.6 Split
      // Horizon。因此，发往各个 interface 的 RIPng 表项是不同的。
      //todo

      for (int i = 0; i < N_IFACE_ON_BOARD; i++) {
        ether_addr mac;
        HAL_GetInterfaceMacAddress(i, &mac);
        ether_addr dest_mac={{0x33,0x33,0x00,0x00,0x00,0x09}};
        send_table(i, eui64(mac),inet6_pton("ff02::9"), dest_mac);
      }
      last_time = time;
    }

    int mask = (1 << N_IFACE_ON_BOARD) - 1;
    ether_addr src_mac;
    ether_addr dst_mac;
    int if_index;
    res = HAL_ReceiveIPPacket(mask, packet, sizeof(packet), &src_mac, &dst_mac,
                              1000, &if_index);
    if (res == HAL_ERR_EOF) {
      break;
    } else if (res < 0) {
      return res;
    } else if (res == 0) {
      // Timeout
      continue;
    } else if (res > sizeof(packet)) {
      // packet is truncated, ignore it
      continue;
    }

    // 检查 IPv6 头部长度
    ip6_hdr *ip6 = (ip6_hdr *)packet;
    if (res < sizeof(ip6_hdr)) {
      printf("Received invalid ipv6 packet (%d < %d)\n", res, sizeof(ip6_hdr));
      continue;
    }
    uint16_t plen = htons(ip6->ip6_plen);
    if (res < plen + sizeof(ip6_hdr)) {
      printf("Received invalid ipv6 packet (%d < %d + %d)\n", res, plen,
             sizeof(ip6_hdr));
      continue;
    }

    // 检查 IPv6 头部目的地址是否为我自己
    bool dst_is_me = false;
    for (int i = 0; i < N_IFACE_ON_BOARD; i++) {
      if (memcmp(&ip6->ip6_dst, &addrs[i], sizeof(in6_addr)) == 0) {
        dst_is_me = true;
        break;
      }
    }

    // TODO: 修改这个检查，当目的地址为 RIPng 的组播目的地址（ff02::9）时也设置
    // dst_is_me 为 true。
    if (ip6->ip6_dst==inet6_pton("ff02::9")) {
      dst_is_me = true;
    }

    if (dst_is_me) {
      // 目的地址是我，按照类型进行处理

      // 检查 checksum 是否正确
      if (ip6->ip6_nxt == IPPROTO_UDP || ip6->ip6_nxt == IPPROTO_ICMPV6) {
        if (!validateAndFillChecksum(packet, res)) {
          printf("Received packet with bad checksum\n");
          continue;
        }
      }

      if (ip6->ip6_nxt == IPPROTO_UDP) {
        // 检查是否为 RIPng packet
        RipPacket rip;
        RipErrorCode err = disassemble(packet, res, &rip);
        if (err == SUCCESS) {
          if (rip.command == 1) {
            // Command 为 Request
            // 参考 RFC 2080 Section 2.4.1 Request Messages 实现
            // 本次实验中，可以简化为只考虑输出完整路由表的情况

            RipPacket resp;
            // 与 5s Timer 时的处理类似，也需要实现水平分割和毒性反转
            // 可以把两部分代码写到单独的函数中
            // 不同的是，在 5s Timer
            // 中要组播发给所有的路由器；这里则是某一个路由器 Request
            // 本路由器，因此回复 Response 的时候，目的 IPv6 地址和 MAC
            // 地址都应该指向发出请求的路由器

            // 最后把 RIPng 包发送出去

            //todo-finish
            ether_addr mac;
            HAL_GetInterfaceMacAddress(if_index,&mac);
            send_table(if_index,eui64(mac),ip6->ip6_src,src_mac);

          } else {
            // Command 为 Response
            // 参考 RFC 2080 Section 2.4.2 Request Messages 实现
            // 按照接受到的 RIPng 表项更新自己的路由表
            // 在本实验中，可以忽略 metric=0xFF 的表项，它表示的是 Nexthop
            // 的设置，可以忽略

            // 接下来的处理中，都首先对输入的 RIPng 表项做如下处理：
            // metric = MIN(metric + cost, infinity)
            // 其中 cost 取 1，表示经过了一跳路由器；infinity 用 16 表示
            // 如果出现了一条新的路由表项，并且 metric 不等于 16：
            // 插入到自己的路由表中，设置 nexthop
            // 地址为发送这个 Response 的路由器。

            // 如果收到的路由表项和已知的重复（注意，是精确匹配），
            // 进行以下的判断：如果路由表中的表项是之前从该路由器从学习而来，那么直接更新
            // metric
            // 为新的值；如果路由表中表现是从其他路由器那里学来，就比较已有的表项和
            // RIPng 表项中的 metric 大小，如果 RIPng 表项中的 metric
            // 更小，说明找到了一条更新的路径，那就用新的表项替换原有的，同时更新
            // nexthop 地址。

            // 可选功能：实现 Triggered
            // Updates，即在路由表出现更新的时候，向所有 interface
            // 发送出现变化的路由表项，注意此时依然要实现水平分割和毒性反转。详见
            // RFC 2080 Section 2.5.1。
            //todo-finish-check
            for (int i = 0; i < rip.numEntries; ++i)
            {
              if(rip.entries[i].metric==0xff){
                continue;
              }
              uint8_t metric = (rip.entries[i].metric+1)>16?16:(rip.entries[i].metric+1);
              bool is_matched= false;

              for(auto item :RT){
                auto entry = item.second;
                if (entry.addr==rip.entries[i].prefix_or_nh&&entry.len==rip.entries[i].prefix_len)
                {
                  is_matched =true;
                  if(entry.nexthop==ip6->ip6_src){
                    entry.metric=metric;
                    entry.if_index=if_index;
                    entry.nexthop= ip6->ip6_src;
                    LEN_ADDR_PAIR la_pair = {entry.len, entry.addr};
                    RT[la_pair]=entry;
                  }
                  else if (entry.metric>metric){
                    auto new_entry = RoutingTableEntry {
                      .addr=rip.entries[i].prefix_or_nh,
                      .len=rip.entries[i].prefix_len,
                      .if_index=if_index,
                      .nexthop=ip6->ip6_src,
                      .route_tag=rip.entries[i].route_tag,
                      .metric=metric
                    };
                    LEN_ADDR_PAIR la_pair = {new_entry.len, new_entry.addr};
                    RT[la_pair]=new_entry;
                  }
                  break;
                }
              }
              if(!is_matched&&metric<16){
                RoutingTableEntry entry;
                entry = RoutingTableEntry{
                  .addr=rip.entries[i].prefix_or_nh,
                  .len=rip.entries[i].prefix_len,
                  .if_index=uint32_t(if_index),
                  .nexthop=ip6->ip6_src,
                  .route_tag=rip.entries[i].route_tag,
                  .metric=metric
                };
                update(1,entry);
              }
            }
         

          }
        } else {
          // 接受到一个错误的 RIPng packet >_<
          printf("Got bad RIP packet from IP %s with error: %s\n",
                 inet6_ntoa(ip6->ip6_src), rip_error_to_string(err));
        }
      } else if (ip6->ip6_nxt == IPPROTO_ICMPV6) {
        // 如果是 ICMPv6 packet
        // 检查是否是 Echo Request

        // 如果是 Echo Request，生成一个对应的 Echo Reply：交换源和目的 IPv6
        // 地址，设置 type 为 Echo Reply，设置 TTL（Hop Limit） 为 64，重新计算
        // Checksum 并发送出去。详见 RFC 4443 Section 4.2 Echo Reply Message
        // todo-finish
        memcpy(output,packet,res);
        icmp6_hdr * icmp6= (icmp6_hdr *)(output + sizeof(ip6_hdr));
        ip6_hdr *new_ip6=(ip6_hdr*)&output[0];
        if(icmp6->icmp6_type==128)
        {
          icmp6->icmp6_type=129;
          new_ip6->ip6_src=ip6->ip6_dst;
          new_ip6->ip6_dst=ip6->ip6_src;
          new_ip6->ip6_hlim=64;
          validateAndFillChecksum(output,res);
          HAL_SendIPPacket(if_index,output,res,src_mac);
        }

      }
      continue;
    } else {
      // 目标地址不是我，考虑转发给下一跳
      // 检查是否是组播地址（ff00::/8），不需要转发组播包
      if (ip6->ip6_dst.s6_addr[0] == 0xff) {
        printf("Don't forward multicast packet to %s\n",
               inet6_ntoa(ip6->ip6_dst));
        continue;
      }

      // 检查 TTL（Hop Limit）是否小于或等于 1
      uint8_t ttl = ip6->ip6_hops;
      if (ttl <= 1) {
        // 发送 ICMP Time Exceeded 消息
        // 将接受到的 IPv6 packet 附在 ICMPv6 头部之后。
        // 如果长度大于 1232 字节，则取前 1232 字节：
        // 1232 = IPv6 Minimum MTU(1280) - IPv6 Header(40) - ICMPv6 Header(8)
        // 意味着发送的 ICMP Time Exceeded packet 大小不大于 IPv6 Minimum MTU
        // 不会因为 MTU 问题被丢弃。
        // 详见 RFC 4443 Section 3.3 Time Exceeded Message
        // 计算 Checksum 后由自己的 IPv6 地址发送给源 IPv6 地址。
        //todo-finish-check
        int packet_len = res>1232?1232:res;
        // IPv6 header
        ip6_hdr *new_ip6 = (ip6_hdr *)&output[0];
        // flow label
        new_ip6->ip6_flow = 0;
        // version
        new_ip6->ip6_vfc = 6 << 4;
        // payload length
        new_ip6->ip6_plen = htons(sizeof(icmp6_hdr)+packet_len);
        // next header
        new_ip6->ip6_nxt = IPPROTO_ICMPV6;
        // hop limit
        new_ip6->ip6_hlim = 255;
        // src ip
        new_ip6->ip6_src = addrs[if_index];
        // dst ip
        new_ip6->ip6_dst = ip6->ip6_src;

        icmp6_hdr *new_icmp6 = (icmp6_hdr *)&output[sizeof(ip6_hdr)];
        new_icmp6->icmp6_type=3;
        new_icmp6->icmp6_code=0;
        new_icmp6->icmp6_cksum=0;

        int hdr_len= sizeof(icmp6_hdr)+sizeof(ip6_hdr);
        memcpy(output+hdr_len,packet,packet_len);

        validateAndFillChecksum(output, packet_len+hdr_len);
        HAL_SendIPPacket(if_index,output,packet_len+hdr_len,src_mac);



      } else {
        // 转发给下一跳
        // 按最长前缀匹配查询路由表
        in6_addr nexthop;
        uint32_t dest_if;
        if (prefix_query(ip6->ip6_dst, &nexthop, &dest_if)) {
          // 找到路由
          ether_addr dest_mac;
          // 如果下一跳为全 0，表示的是直连路由，目的机器和本路由器可以直接访问
          if (nexthop == in6_addr{0}) {
            nexthop = ip6->ip6_dst;
          }
          if (HAL_GetNeighborMacAddress(dest_if, nexthop, &dest_mac) == 0) {
            // 在 NDP 表中找到了下一跳的 MAC 地址
            // TTL-1
            ip6->ip6_hops--;

            // 转发出去
            memcpy(output, packet, res);
            HAL_SendIPPacket(dest_if, output, res, dest_mac);
          } else {
            // 没有找到下一跳的 MAC 地址
            // 本实验中可以直接丢掉，等对方回复 NDP 之后，再恢复正常转发。
            printf("Nexthop ip %s is not found in NDP table\n",
                   inet6_ntoa(nexthop));
          }
        } else {
          // 没有找到路由
          // 发送 ICMPv6 Destination Unreachable 消息
          // 要求与上面发送 ICMPv6 Time Exceeded 消息一致
          // Code 取 0，表示 No route to destination
          // 详见 RFC 4443 Section 3.1 Destination Unreachable Message
          // 计算 Checksum 后由自己的 IPv6 地址发送给源 IPv6 地址。
          //todo-finish-check
          int packet_len = res>1232?1232:res;
          // IPv6 header
          ip6_hdr *new_ip6 = (ip6_hdr *)&output[0];
          // flow label
          new_ip6->ip6_flow = 0;
          // version
          new_ip6->ip6_vfc = 6 << 4;
          // payload length
          new_ip6->ip6_plen = htons(sizeof(icmp6_hdr)+packet_len);
          // next header
          new_ip6->ip6_nxt = IPPROTO_ICMPV6;
          // hop limit
          new_ip6->ip6_hlim = 255;
          // src ip
          new_ip6->ip6_src = addrs[if_index];
          // dst ip
          new_ip6->ip6_dst = ip6->ip6_src;

          icmp6_hdr *new_icmp6 = (icmp6_hdr *)&output[sizeof(ip6_hdr)];
          new_icmp6->icmp6_type=1;
          new_icmp6->icmp6_code=0;
          new_icmp6->icmp6_cksum=0;

          int hdr_len= sizeof(icmp6_hdr)+sizeof(ip6_hdr);
          memcpy(output+hdr_len,packet,packet_len);

          validateAndFillChecksum(output, packet_len+hdr_len);
          HAL_SendIPPacket(if_index,output,packet_len+hdr_len,src_mac);


          printf("Destination IP %s not found in routing table",
                 inet6_ntoa(ip6->ip6_dst));
          printf(" and source IP is %s\n", inet6_ntoa(ip6->ip6_src));
        }
      }
    }
  }
  return 0;
}
