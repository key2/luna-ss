Protocol Layer

### 8.4 Link Management Packet (LMP)

Packets that have the Type field set to Link Management Packet are referred to as LMPs. These packets are used to manage a single link. They carry no addressing information and as such are not routable. They may be generated as the result of hub port commands. For example, a hub port command is used to set the U2 inactivity timeout. In addition, they are used to exchange port capability information and may be used for testing purposes.

![img-190.jpeg](img-190.jpeg)

Figure 8-4. Link Management Packet Structure

#### 8.4.1 Subtype Field

The value in the LMP Subtype field further identifies the content of the LMP.

Table 8-3. Link Management Packet Subtype Field

[tbl-106.md](tbl-106.md)

8-7