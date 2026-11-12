"""Kaggle Notebook 模板 — 拷进 Notebook 用
免费档：每周 30 小时 GPU，T4 x2，单次最长 12 小时
用法：Settings > Accelerator 选 GPU T4 x2，Internet 开
跑法：Save & Run All / Commit，后台跑，关浏览器继续跑
保存：只留 /kaggle/working 内 20GB，其余会话结束即删
注意：两张 T4 是独立卡，不是 32GB 单卡；单卡 >16GB 的模型跑不了
"""
import os, torch

print("torch", torch.__version__)
print("cuda available:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("device count:", torch.cuda.device_count())
    for i in range(torch.cuda.device_count()):
        print(i, torch.cuda.get_device_name(i))

OUT = "/kaggle/working"
os.makedirs(OUT, exist_ok=True)

# TODO: 在这里放你的训练 / 推理代码
# 产出写到 OUT，例如：
# torch.save(model.state_dict(), f"{OUT}/model.pt")
# with open(f"{OUT}/result.json", "w") as f: json.dump(result, f)

print("输出目录:", OUT, os.listdir(OUT))
