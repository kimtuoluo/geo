from osgeo import gdal

# 启用 GDAL 异常处理
gdal.UseExceptions()

# 打开 DSM 文件
file_path = "output_heights.tif"  # 替换为你的实际文件路径
ds = gdal.Open(file_path)

if ds is None:
    raise FileNotFoundError(f"无法打开文件：{file_path}")

# 获取第一个波段
band = ds.GetRasterBand(1)  # 注意这里是 GetRasterBand，而不是 GetRasterBandtif
if band is None:
    raise ValueError("未能获取波段，请检查文件格式和内容。")

# 打印波段信息
print(f"波段数据类型: {gdal.GetDataTypeName(band.DataType)}")
#适用于已经有元数据直接读取波段统计数据的情况
#print(f"波段最小值: {band.GetMinimum()}")
#print(f"波段最大值: {band.GetMaximum()}")

# 计算统计信息（包括最小值和最大值）
# 调用这个方法后，会计算波段的统计信息，把结果保存在.aux.xml文件中
band.ComputeStatistics(False)

# 再次获取最小值和最大值
min_value = band.GetMinimum()
max_value = band.GetMaximum()

# 打印结果
print(f"波段最小值: {min_value}")
print(f"波段最大值: {max_value}")

# 将数据保存为 16 位 PNG：
gdal.Translate("output_heights_16bit.png", ds, format="PNG", outputType=gdal.GDT_UInt16)
