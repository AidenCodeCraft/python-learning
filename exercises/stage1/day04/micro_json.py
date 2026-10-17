# 练 A1：写 to_json(obj: object) -> str，返回不转义中文的 JSON 字符串。 
import json

def to_json(obj: object) -> str:
    return json.dumps(obj, ensure_ascii=False)

# 练 A2：写 save_json(path: str, obj: object) -> None 和 load_json(path: str) -> object（load_json 在文件不存在时返回 None）。 

def save_json(path: str, obj: object) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)

def load_json(path: str) -> object:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

# 练 A3（改错 + 说结果）：下面哪几行会报错？为什么？
# json.dumps({"a": {1, 2}})          # ① set 不能序列化
# json.dumps({"a": (1, 2)})          # ② 正常，元组被当成 array 输出 [1, 2]。
# json.loads(json.dumps({"a": (1, 2)}))   # ③ 结果是？元组会变成list {'a': [1, 2]}
# json.dumps({(1, 2): "a"})          # ④ TypeError: keys must be str, int, float, bool or None, not tuple

if __name__ == "__main__":
    print("A1:", to_json({"name": "汤姆"}))
    save_json(".tmp/chk.json", {"a": 1})
    print("A2:", load_json(".tmp/chk.json"), load_json(".tmp/nope.json"))
    # 期望： A1: {"name": "汤姆"}    A2: {'a': 1} None