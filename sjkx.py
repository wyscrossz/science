import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# ====================== 字体与设置 ======================
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']  # 中文正常显示，备选字体用于特殊符号
plt.rcParams['axes.unicode_minus'] = False

# ====================== 读取真实空气质量数据 ======================
data_path = "air_quality_real_data.csv"

if not os.path.exists(data_path):
    print(f"❌ 未找到数据文件！请确保 {data_path} 和本代码在同一个文件夹")
else:
    df = pd.read_csv(data_path, encoding="utf-8-sig")
    print(f"✅ 成功读取真实数据文件：{data_path}")
    print(f"✅ 数据包含 {len(df)} 个城市，{len(df.columns)} 个字段")

    # ====================== 数据清洗 ======================
    numeric_cols = ["AQI", "PM2.5", "PM10", "SO2", "NO2", "O3"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df[(df["AQI"] >= 0) & (df["AQI"] <= 500)]
    print("✅ 数据清洗完成，可用于分析")

    # ====================== 图表1：全国城市空气质量等级占比饼图 ======================
    plt.figure(figsize=(7, 7))
    level_count = df["等级"].value_counts()
    level_count.plot(kind="pie", autopct="%1.1f%%", startangle=90,
                     colors=["#2E8B57", "#FFD700", "#FFA500", "#DC143C"])
    plt.title("全国城市空气质量等级占比", fontsize=14, pad=20)
    plt.savefig("1_等级饼图.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("✅ 图表1：等级饼图已生成")

    # ====================== 图表2：各省份平均AQI柱状图（前10名） ======================
    prov_aqi = df.groupby("省份")["AQI"].mean().sort_values(ascending=False).head(10)
    plt.figure(figsize=(12, 5))
    sns.barplot(x=prov_aqi.index, y=prov_aqi.values, hue=prov_aqi.index,
                palette="RdYlGn_r", legend=False)
    plt.title("各省份平均AQI（前10名）", fontsize=14, pad=20)
    plt.xlabel("省份", fontsize=12)
    plt.ylabel("AQI均值", fontsize=12)
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig("2_省份AQI柱状图.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("✅ 图表2：省份AQI柱状图已生成")

    # ====================== 图表3：污染物相关性热力图 ======================
    corr = df[numeric_cols].corr()
    plt.figure(figsize=(9, 7))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
    plt.title("污染物相关性热力图", fontsize=14, pad=20)
    plt.tight_layout()
    plt.savefig("3_相关性热力图.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("✅ 图表3：相关性热力图已生成")

    # ====================== 图表4：不同等级PM2.5浓度箱线图（修复字体警告） ======================
    plt.figure(figsize=(10, 5))
    sns.boxplot(x="等级", y="PM2.5", data=df, hue="等级", palette="RdYlGn", legend=False)
    plt.title("不同空气质量等级PM2.5浓度分布", fontsize=14, pad=20)
    plt.xlabel("空气质量等级", fontsize=12)
    # ↓ 修改处：用 $^3$ 生成上标，避免字体缺失警告
    plt.ylabel("PM2.5浓度（μg/m$^3$）", fontsize=12)
    plt.tight_layout()
    plt.savefig("4_PM25箱线图.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("✅ 图表4：PM25箱线图已生成")

    # ====================== 图表5：全国城市AQI指数分布直方图 ======================
    plt.figure(figsize=(9, 5))
    sns.histplot(df["AQI"], kde=True, color="skyblue", bins=20)
    plt.title("全国城市AQI指数分布", fontsize=14, pad=20)
    plt.xlabel("AQI指数", fontsize=12)
    plt.ylabel("城市数量", fontsize=12)
    plt.axvline(df["AQI"].mean(), color="red", linestyle="--",
                label=f"均值：{df['AQI'].mean():.1f}")
    plt.legend()
    plt.tight_layout()
    plt.savefig("5_AQI直方图.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("✅ 图表5：AQI直方图已生成")

    # ====================== 图表6：南北方污染物均值对比柱状图（修复字体警告） ======================
    northern_provinces = ["北京", "天津", "河北", "山西", "内蒙古", "辽宁", "吉林", "黑龙江", "山东", "河南"]
    df["区域"] = df["省份"].apply(lambda x: "北方" if x in northern_provinces else "南方")
    cols = ["PM2.5", "PM10", "SO2", "NO2", "O3"]
    mean_df = df.groupby("区域")[cols].mean().T
    plt.figure(figsize=(11, 5))
    mean_df.plot(kind="bar", width=0.6, color=["#FF6B6B", "#4ECDC4"])
    plt.title("南北方污染物均值对比", fontsize=14, pad=20)
    plt.xlabel("污染物类型", fontsize=12)
    # ↓ 修改处：用 $^3$ 生成上标
    plt.ylabel("浓度均值（μg/m$^3$）", fontsize=12)
    plt.legend(title="区域")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("6_南北对比柱状图.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("✅ 图表6：南北对比柱状图已生成")

    print("\n🎉 全部完成！生成文件如下（均可直接用于论文、上传Github）：")
    print("1. 真实数据文件：air_quality_real_data.csv")
    print("2. 6张高清图表：1_等级饼图.png ~ 6_南北对比柱状图.png")
    print("3. 可运行代码：air_quality_run.py")