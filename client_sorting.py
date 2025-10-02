def classify_by_amount(amount):
    if amount < 100:
        return "Дрібнота"
    elif 100 <= amount <= 999:
        return "Середнячок"
    else:
        return "Великий клієнт"


def classify_by_status(status):
    match status:
        case "clean":
            return "Працювати без питань"
        case "suspicious":
            return "Перевірити документи"
        case "fraud":
            return "У чорний список"
        case _:
            return "Невідомий статус"


def process_clients(clients):
    results = []
    
    for client in clients:
        name = client.get("ім'я", "Без імені")
        amount = client.get("сума угоди")
        status = client.get("статус перевірки", "")

        if not isinstance(amount, (int, float)):
            results.append({
                "ім'я": name,
                "результат": "Фальшиві дані"
            })
            continue

        amount_category = classify_by_amount(amount)
        status_decision = classify_by_status(status)
        results.append({
            "ім'я": name,
            "категорія": amount_category,
            "рішення": status_decision,
            "сума": amount
        })
    
    return results


def print_results(results):
    print("=" * 80)
    print("РЕЗУЛЬТАТ")
    print("=" * 80)
    
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['ім\'я']}")
        
        if result.get('результат') == "Фальшиві дані":
            print(f"   {result['результат']}")
        else:
            print(f"   Сума: {result['сума']}")
            print(f"   Категорія: {result['категорія']}")
            print(f"   Рішення: {result['рішення']}")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    test_clients = [
        {
            "ім'я": "Іван Петренко",
            "сума угоди": 1500,
            "статус перевірки": "clean"
        },
        {
            "ім'я": "Марія Коваленко",
            "сума угоди": 50,
            "статус перевірки": "suspicious"
        },
        {
            "ім'я": "Олександр Шевченко",
            "сума угоди": 750.50,
            "статус перевірки": "clean"
        },
        {
            "ім'я": "Анна Мельник",
            "сума угоди": "не число",
            "статус перевірки": "clean"
        },
        {
            "ім'я": "Дмитро Бондаренко",
            "сума угоди": 5000,
            "статус перевірки": "fraud"
        },
        {
            "ім'я": "Олена Сидоренко",
            "сума угоди": 200,
            "статус перевірки": "unknown"
        },
        {
            "ім'я": "Петро Ткаченко",
            "сума угоди": 99.99,
            "статус перевірки": "clean"
        }
    ]

    results = process_clients(test_clients)
    print_results(results)
    print("\nСТАТИСТИКА:")
    valid_results = [r for r in results if 'категорія' in r]
    
    if valid_results:
        categories = {}
        decisions = {}
        
        for r in valid_results:
            cat = r['категорія']
            dec = r['рішення']
            categories[cat] = categories.get(cat, 0) + 1
            decisions[dec] = decisions.get(dec, 0) + 1
        
        print("\nКатегорії клієнтів:")
        for cat, count in categories.items():
            print(f"  • {cat}: {count}")
        
        print("\nРішення за статусами:")
        for dec, count in decisions.items():
            print(f"  • {dec}: {count}")
    
    invalid_count = len([r for r in results if r.get('результат') == "Фальшиві дані"])
    if invalid_count > 0:
        print(f"\nФальшиві дані: {invalid_count}")
