//  三角数系CAC编码
//  
//  1. Design Sources
//  
//      1.1 TNS.vh
//          与TNS数系有关的定义
//      1.2 FNS.vh
//          与FNS数系有关的定义，以及与IDP/3D-DPS编码有关的定义
//      1.3 TNS_encoder_xx/TNS_dec_xx
//          TNS编解码器，xx为编码长度
//      1.4 FPF_encoder_xx/FNS_dec_xx
//          FNS FPF编解码器，xx为编码长度
//      1.5 FTF_encoder_xx/FNS_dec_xx
//          FNS FTF编解码器，xx为编码长度
//      1.6 IDP_encoder_xx/IDP_dec_xx
//          IDP编解码器，xx为编码长度
//      1.7 DPS_encoder_xx/DPS_dec_xx
//          3D-DPS编解码器，xx为编码长度
//  2. Simulation Sources
//
//      2.1 Simu_TNS_xx
//          验证TNS编解码功能
//      2.2 Simu_FPF_xx
//          验证FPF编解码功能
//      2.3 Simu_FTF_xx
//          验证FTF编解码功能
//      2.4 Simu_IDP_xx
//          验证IDP编解码功能
//      2.5 Simu_DPS_xx
//          验证3D-DPS编解码功能
//
//
//
//  3. Revision
//
//      【2020.05.14】 - 初版
//      【2020.06.06】 - 编码部分长度的数据时，各种编码所需的最小码字长度
//                          Datalen:    5   8   11  14  17  20  23  26  29
//                          TNS:        6   9   12  15  19  22  25  28  31
//                          FNS:        7   12  16  20  25  29  33  38  42
//                          3DDPS:      7   11  16  20  24  29  33  37  42
//                          IDP:        7   11  16  20  24  29  33  37  42