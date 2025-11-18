#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双一流大学完整名单及官网地址
"""

# 147所双一流大学名单及官网
DOUBLE_FIRST_CLASS_UNIVERSITIES = {
    # 北京地区（30所）
    '北京大学': 'https://www.pku.edu.cn',
    '中国人民大学': 'https://www.ruc.edu.cn',
    '清华大学': 'https://www.tsinghua.edu.cn',
    '北京交通大学': 'https://www.bjtu.edu.cn',
    '北京工业大学': 'https://www.bjut.edu.cn',
    '北京航空航天大学': 'https://www.buaa.edu.cn',
    '北京理工大学': 'https://www.bit.edu.cn',
    '北京科技大学': 'https://www.ustb.edu.cn',
    '北京化工大学': 'https://www.buct.edu.cn',
    '北京邮电大学': 'https://www.bupt.edu.cn',
    '中国农业大学': 'https://www.cau.edu.cn',
    '北京林业大学': 'https://www.bjfu.edu.cn',
    '北京协和医学院': 'https://www.pumc.edu.cn',
    '北京中医药大学': 'https://www.bucm.edu.cn',
    '北京师范大学': 'https://www.bnu.edu.cn',
    '首都师范大学': 'https://www.cnu.edu.cn',
    '北京外国语大学': 'https://www.bfsu.edu.cn',
    '中国传媒大学': 'https://www.cuc.edu.cn',
    '中央财经大学': 'https://www.cufe.edu.cn',
    '对外经济贸易大学': 'https://www.uibe.edu.cn',
    '外交学院': 'https://www.cfau.edu.cn',
    '中国人民公安大学': 'https://www.ppsuc.edu.cn',
    '北京体育大学': 'https://www.bsu.edu.cn',
    '中央音乐学院': 'https://www.ccom.edu.cn',
    '中国音乐学院': 'https://www.ccmusic.edu.cn',
    '中央美术学院': 'https://www.cafa.edu.cn',
    '中央戏剧学院': 'https://www.zhongxi.cn',
    '中央民族大学': 'https://www.muc.edu.cn',
    '中国政法大学': 'https://www.cupl.edu.cn',
    '中国科学院大学': 'https://www.ucas.ac.cn',

    # 天津地区（5所）
    '南开大学': 'https://www.nankai.edu.cn',
    '天津大学': 'https://www.tju.edu.cn',
    '天津工业大学': 'https://www.tiangong.edu.cn',
    '天津医科大学': 'https://www.tmu.edu.cn',
    '天津中医药大学': 'https://www.tjutcm.edu.cn',

    # 河北、山西、内蒙古地区（5所）
    '华北电力大学': 'https://www.ncepu.edu.cn',
    '河北工业大学': 'https://www.hebut.edu.cn',
    '山西大学': 'https://www.sxu.edu.cn',
    '太原理工大学': 'https://www.tyut.edu.cn',
    '内蒙古大学': 'https://www.imu.edu.cn',

    # 东北地区（11所）
    '辽宁大学': 'https://www.lnu.edu.cn',
    '大连理工大学': 'https://www.dlut.edu.cn',
    '东北大学': 'https://www.neu.edu.cn',
    '大连海事大学': 'https://www.dlmu.edu.cn',
    '吉林大学': 'https://www.jlu.edu.cn',
    '延边大学': 'https://www.ybu.edu.cn',
    '东北师范大学': 'https://www.nenu.edu.cn',
    '哈尔滨工业大学': 'https://www.hit.edu.cn',
    '哈尔滨工程大学': 'https://www.hrbeu.edu.cn',
    '东北农业大学': 'https://www.neau.edu.cn',
    '东北林业大学': 'https://www.nefu.edu.cn',

    # 上海地区（15所）
    '复旦大学': 'https://www.fudan.edu.cn',
    '同济大学': 'https://www.tongji.edu.cn',
    '上海交通大学': 'https://www.sjtu.edu.cn',
    '华东理工大学': 'https://www.ecust.edu.cn',
    '东华大学': 'https://www.dhu.edu.cn',
    '上海海洋大学': 'https://www.shou.edu.cn',
    '上海中医药大学': 'https://www.shutcm.edu.cn',
    '华东师范大学': 'https://www.ecnu.edu.cn',
    '上海外国语大学': 'https://www.shisu.edu.cn',
    '上海财经大学': 'https://www.sufe.edu.cn',
    '上海体育学院': 'https://www.sus.edu.cn',
    '上海音乐学院': 'https://www.shcmusic.edu.cn',
    '上海大学': 'https://www.shu.edu.cn',
    '南方科技大学': 'https://www.sustech.edu.cn',
    '上海科技大学': 'https://www.shanghaitech.edu.cn',

    # 江苏地区（16所）
    '南京大学': 'https://www.nju.edu.cn',
    '苏州大学': 'https://www.suda.edu.cn',
    '东南大学': 'https://www.seu.edu.cn',
    '南京航空航天大学': 'https://www.nuaa.edu.cn',
    '南京理工大学': 'https://www.njust.edu.cn',
    '中国矿业大学': 'https://www.cumt.edu.cn',
    '南京邮电大学': 'https://www.njupt.edu.cn',
    '河海大学': 'https://www.hhu.edu.cn',
    '江南大学': 'https://www.jiangnan.edu.cn',
    '南京林业大学': 'https://www.njfu.edu.cn',
    '南京信息工程大学': 'https://www.nuist.edu.cn',
    '南京农业大学': 'https://www.njau.edu.cn',
    '南京医科大学': 'https://www.njmu.edu.cn',
    '南京中医药大学': 'https://www.njucm.edu.cn',
    '中国药科大学': 'https://www.cpu.edu.cn',
    '南京师范大学': 'https://www.njnu.edu.cn',

    # 浙江地区（3所）
    '浙江大学': 'https://www.zju.edu.cn',
    '中国美术学院': 'https://www.caa.edu.cn',
    '宁波大学': 'https://www.nbu.edu.cn',

    # 安徽地区（3所）
    '安徽大学': 'https://www.ahu.edu.cn',
    '中国科学技术大学': 'https://www.ustc.edu.cn',
    '合肥工业大学': 'https://www.hfut.edu.cn',

    # 福建地区（2所）
    '厦门大学': 'https://www.xmu.edu.cn',
    '福州大学': 'https://www.fzu.edu.cn',

    # 江西地区（1所）
    '南昌大学': 'https://www.ncu.edu.cn',

    # 山东地区（3所）
    '山东大学': 'https://www.sdu.edu.cn',
    '中国海洋大学': 'https://www.ouc.edu.cn',
    '中国石油大学（华东）': 'https://www.upc.edu.cn',

    # 河南地区（2所）
    '郑州大学': 'https://www.zzu.edu.cn',
    '河南大学': 'https://www.henu.edu.cn',

    # 湖北地区（7所）
    '武汉大学': 'https://www.whu.edu.cn',
    '华中科技大学': 'https://www.hust.edu.cn',
    '中国地质大学（武汉）': 'https://www.cug.edu.cn',
    '武汉理工大学': 'https://www.whut.edu.cn',
    '华中农业大学': 'https://www.hzau.edu.cn',
    '华中师范大学': 'https://www.ccnu.edu.cn',
    '中南财经政法大学': 'https://www.zuel.edu.cn',

    # 湖南地区（4所）
    '湘潭大学': 'https://www.xtu.edu.cn',
    '湖南大学': 'https://www.hnu.edu.cn',
    '中南大学': 'https://www.csu.edu.cn',
    '湖南师范大学': 'https://www.hunnu.edu.cn',

    # 广东地区（7所）
    '中山大学': 'https://www.sysu.edu.cn',
    '暨南大学': 'https://www.jnu.edu.cn',
    '华南理工大学': 'https://www.scut.edu.cn',
    '华南农业大学': 'https://www.scau.edu.cn',
    '广州医科大学': 'https://www.gzhmu.edu.cn',
    '广州中医药大学': 'https://www.gzucm.edu.cn',
    '华南师范大学': 'https://www.scnu.edu.cn',

    # 海南、广西地区（2所）
    '海南大学': 'https://www.hainanu.edu.cn',
    '广西大学': 'https://www.gxu.edu.cn',

    # 四川、重庆地区（8所）
    '四川大学': 'https://www.scu.edu.cn',
    '重庆大学': 'https://www.cqu.edu.cn',
    '西南交通大学': 'https://www.swjtu.edu.cn',
    '电子科技大学': 'https://www.uestc.edu.cn',
    '西南石油大学': 'https://www.swpu.edu.cn',
    '成都理工大学': 'https://www.cdut.edu.cn',
    '四川农业大学': 'https://www.sicau.edu.cn',
    '成都中医药大学': 'https://www.cdutcm.edu.cn',

    # 云贵地区（4所）
    '西南大学': 'https://www.swu.edu.cn',
    '西南财经大学': 'https://www.swufe.edu.cn',
    '贵州大学': 'https://www.gzu.edu.cn',
    '云南大学': 'https://www.ynu.edu.cn',

    # 西藏地区（1所）
    '西藏大学': 'https://www.utibet.edu.cn',

    # 陕西地区（7所）
    '西北大学': 'https://www.nwu.edu.cn',
    '西安交通大学': 'https://www.xjtu.edu.cn',
    '西北工业大学': 'https://www.nwpu.edu.cn',
    '西安电子科技大学': 'https://www.xidian.edu.cn',
    '长安大学': 'https://www.chd.edu.cn',
    '西北农林科技大学': 'https://www.nwafu.edu.cn',
    '陕西师范大学': 'https://www.snnu.edu.cn',

    # 甘肃、青海、宁夏、新疆地区（6所）
    '兰州大学': 'https://www.lzu.edu.cn',
    '青海大学': 'https://www.qhu.edu.cn',
    '宁夏大学': 'https://www.nxu.edu.cn',
    '新疆大学': 'https://www.xju.edu.cn',
    '石河子大学': 'https://www.shzu.edu.cn',

    # 特殊机构（5所）
    '中国矿业大学（北京）': 'https://www.cumtb.edu.cn',
    '中国石油大学（北京）': 'https://www.cup.edu.cn',
    '中国地质大学（北京）': 'https://www.cugb.edu.cn',
    '国防科技大学': 'https://www.nudt.edu.cn',
    '海军军医大学': 'https://www.smmu.edu.cn',
    # '空军军医大学': 'https://www.fmmu.edu.cn',  # 官网可能有变化
}

def get_all_universities():
    """获取所有双一流大学列表"""
    return list(DOUBLE_FIRST_CLASS_UNIVERSITIES.keys())

def get_university_url(university_name):
    """获取指定大学的官网地址"""
    return DOUBLE_FIRST_CLASS_UNIVERSITIES.get(university_name, '')

if __name__ == '__main__':
    print(f"双一流大学总数: {len(DOUBLE_FIRST_CLASS_UNIVERSITIES)}")
    print("\n所有大学:")
    for i, uni in enumerate(get_all_universities(), 1):
        print(f"{i}. {uni} - {get_university_url(uni)}")
