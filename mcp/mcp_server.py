"""
Dining ROI MCP server (stdio, JSON-RPC 2.0).

A zero-dependency (stdlib-only) Model Context Protocol server for the
"Dining ROI" demo. It exposes the menu, the per-dish ingredient
decompositions, the wholesale ingredient costs, and a deterministic
menu analysis that ranks dishes by markup_multiple (menu_price /
food_cost) -- lower multiple means better value for the diner.

The menu data is baked directly into this file as a Python dict
literal, so the server is fully self-contained and cwd-independent;
nothing is read from disk at runtime.
"""

import json
import sys

MENU = {   'restaurant': "Hal's",
    'dishes': [   {   'id': 'crab-cakes',
                      'name': 'Jumbo Lump Crab Cakes',
                      'category': 'Starters',
                      'menu_price': 34,
                      'description': 'Two seared cakes of all jumbo lump crab, barely bound, '
                                     'Creole remoulade.',
                      'ingredients': [   {'ingredient': 'lump crab meat', 'qty': 6, 'unit': 'oz'},
                                         {'ingredient': 'egg', 'qty': 0.5, 'unit': 'each'},
                                         {'ingredient': 'butter', 'qty': 1, 'unit': 'oz'}]},
                  {   'id': 'seafood-gumbo',
                      'name': 'Seafood Gumbo',
                      'category': 'Starters',
                      'menu_price': 24,
                      'description': 'Dark roux, crawfish and andouille, okra and rice, a New '
                                     'Orleans bowl.',
                      'ingredients': [   {'ingredient': 'crab roux base', 'qty': 4, 'unit': 'oz'},
                                         {'ingredient': 'okra', 'qty': 3, 'unit': 'oz'},
                                         {'ingredient': 'crawfish tail', 'qty': 2, 'unit': 'oz'},
                                         {   'ingredient': 'andouille sausage',
                                             'qty': 2,
                                             'unit': 'oz'},
                                         {'ingredient': 'rice', 'qty': 4, 'unit': 'oz'}]},
                  {   'id': 'hals-wedge',
                      'name': "Hal's Wedge",
                      'category': 'Salads',
                      'menu_price': 15,
                      'description': 'Iceberg wedge, Maytag blue, smoked bacon, vine tomato, blue '
                                     'cheese dressing.',
                      'ingredients': [   {'ingredient': 'iceberg wedge', 'qty': 1, 'unit': 'each'},
                                         {'ingredient': 'blue cheese', 'qty': 2, 'unit': 'oz'},
                                         {'ingredient': 'bacon', 'qty': 1, 'unit': 'oz'},
                                         {'ingredient': 'tomato', 'qty': 2, 'unit': 'oz'}]},
                  {   'id': 'caesar-salad',
                      'name': 'Caesar Salad',
                      'category': 'Salads',
                      'menu_price': 15,
                      'description': 'Crisp romaine hearts, garlic croutons, anchovy, shaved '
                                     'parmesan.',
                      'ingredients': [   {'ingredient': 'romaine heart', 'qty': 1, 'unit': 'each'},
                                         {'ingredient': 'parmesan', 'qty': 1, 'unit': 'oz'},
                                         {'ingredient': 'croutons', 'qty': 1, 'unit': 'oz'},
                                         {'ingredient': 'anchovy', 'qty': 0.3, 'unit': 'oz'}]},
                  {   'id': 'bone-in-prime-ribeye',
                      'name': 'Bone-in Prime Ribeye',
                      'category': 'Steaks & Chops',
                      'menu_price': 68,
                      'description': '28 oz USDA Prime bone-in ribeye, hard-seared, finished with '
                                     'herb butter.',
                      'ingredients': [   {   'ingredient': 'prime ribeye bone-in',
                                             'qty': 28,
                                             'unit': 'oz'},
                                         {'ingredient': 'butter', 'qty': 1, 'unit': 'oz'}]},
                  {   'id': 'ny-strip',
                      'name': 'New York Strip',
                      'category': 'Steaks & Chops',
                      'menu_price': 52,
                      'description': "14 oz center-cut strip, charred crust, maitre d' butter.",
                      'ingredients': [   {'ingredient': 'ny strip steak', 'qty': 14, 'unit': 'oz'},
                                         {'ingredient': 'butter', 'qty': 1, 'unit': 'oz'}]},
                  {   'id': 'filet-mignon',
                      'name': 'Filet Mignon',
                      'category': 'Steaks & Chops',
                      'menu_price': 60,
                      'description': '9 oz center-cut tenderloin, the house indulgence, '
                                     'butter-basted.',
                      'ingredients': [   {'ingredient': 'filet mignon', 'qty': 9, 'unit': 'oz'},
                                         {'ingredient': 'butter', 'qty': 1, 'unit': 'oz'}]},
                  {   'id': 'whole-branzino',
                      'name': 'Whole Roasted Branzino',
                      'category': 'Seafood',
                      'menu_price': 46,
                      'description': 'Whole Mediterranean branzino, roasted on the bone, garlic '
                                     'and lemon butter.',
                      'ingredients': [   {'ingredient': 'branzino whole', 'qty': 1, 'unit': 'each'},
                                         {'ingredient': 'butter', 'qty': 1, 'unit': 'oz'},
                                         {'ingredient': 'garlic', 'qty': 0.5, 'unit': 'oz'}]},
                  {   'id': 'gulf-shrimp-creole',
                      'name': 'Gulf Shrimp Creole',
                      'category': 'Seafood',
                      'menu_price': 33,
                      'description': 'Gulf white shrimp, Creole tomato gravy, over steamed rice.',
                      'ingredients': [   {'ingredient': 'gulf shrimp', 'qty': 8, 'unit': 'oz'},
                                         {'ingredient': 'tomato', 'qty': 4, 'unit': 'oz'},
                                         {'ingredient': 'rice', 'qty': 6, 'unit': 'oz'},
                                         {'ingredient': 'crab roux base', 'qty': 2, 'unit': 'oz'}]},
                  {   'id': 'lobster-mac-and-cheese',
                      'name': 'Lobster Mac & Cheese',
                      'category': 'Pasta & Entrees',
                      'menu_price': 29,
                      'description': 'Cavatappi in a three-cheese cream, folded with '
                                     'butter-poached lobster.',
                      'ingredients': [   {'ingredient': 'lobster meat', 'qty': 4, 'unit': 'oz'},
                                         {'ingredient': 'cavatappi pasta', 'qty': 4, 'unit': 'oz'},
                                         {'ingredient': 'parmesan', 'qty': 2, 'unit': 'oz'},
                                         {'ingredient': 'heavy cream', 'qty': 3, 'unit': 'oz'},
                                         {'ingredient': 'butter', 'qty': 1, 'unit': 'oz'}]},
                  {   'id': 'cacio-e-pepe',
                      'name': 'Cacio e Pepe',
                      'category': 'Pasta & Entrees',
                      'menu_price': 31,
                      'description': 'House spaghetti, pecorino romano, cracked black pepper. '
                                     'Simple, Roman.',
                      'ingredients': [   {'ingredient': 'dry spaghetti', 'qty': 5, 'unit': 'oz'},
                                         {   'ingredient': 'pecorino romano',
                                             'qty': 2.5,
                                             'unit': 'oz'}]},
                  {   'id': 'creamed-spinach',
                      'name': 'Creamed Spinach',
                      'category': 'Sides',
                      'menu_price': 14,
                      'description': 'Baby spinach folded into a rich butter cream.',
                      'ingredients': [   {'ingredient': 'baby spinach', 'qty': 6, 'unit': 'oz'},
                                         {'ingredient': 'heavy cream', 'qty': 3, 'unit': 'oz'},
                                         {'ingredient': 'butter', 'qty': 1, 'unit': 'oz'}]},
                  {   'id': 'truffle-fries',
                      'name': 'Truffle Fries',
                      'category': 'Sides',
                      'menu_price': 15,
                      'description': 'Hand-cut fries, black truffle oil, shaved parmesan.',
                      'ingredients': [   {'ingredient': 'russet potato', 'qty': 8, 'unit': 'oz'},
                                         {   'ingredient': 'black truffle oil',
                                             'qty': 1,
                                             'unit': 'tbsp'},
                                         {'ingredient': 'parmesan', 'qty': 1, 'unit': 'oz'}]},
                  {   'id': 'old-fashioned',
                      'name': "Hal's Old Fashioned",
                      'category': 'Cocktails',
                      'menu_price': 18,
                      'description': 'Bourbon, demerara, aromatic bitters, orange.',
                      'ingredients': [   {'ingredient': 'bourbon', 'qty': 2.5, 'unit': 'oz'},
                                         {'ingredient': 'simple syrup', 'qty': 0.25, 'unit': 'oz'},
                                         {'ingredient': 'bitters', 'qty': 0.1, 'unit': 'oz'}]},
                  {   'id': 'espresso-martini',
                      'name': 'Espresso Martini',
                      'category': 'Cocktails',
                      'menu_price': 18,
                      'description': 'Vodka, fresh espresso, coffee liqueur, shaken to a foam.',
                      'ingredients': [   {'ingredient': 'vodka', 'qty': 2, 'unit': 'oz'},
                                         {'ingredient': 'espresso', 'qty': 1, 'unit': 'oz'},
                                         {'ingredient': 'coffee liqueur', 'qty': 1, 'unit': 'oz'}]},
                  {   'id': 'bread-pudding',
                      'name': 'Bourbon Bread Pudding',
                      'category': 'Dessert',
                      'menu_price': 15,
                      'description': 'Brioche custard, vanilla bean, warm bourbon sauce.',
                      'ingredients': [   {'ingredient': 'brioche bread', 'qty': 5, 'unit': 'oz'},
                                         {'ingredient': 'heavy cream', 'qty': 3, 'unit': 'oz'},
                                         {'ingredient': 'egg', 'qty': 2, 'unit': 'each'},
                                         {   'ingredient': 'vanilla bean',
                                             'qty': 0.25,
                                             'unit': 'each'}]}],
    'ingredient_costs': {   'lump crab meat': {'unit_cost': 2.55, 'unit': 'oz'},
                            'lobster meat': {'unit_cost': 2.1, 'unit': 'oz'},
                            'prime ribeye bone-in': {'unit_cost': 1.05, 'unit': 'oz'},
                            'ny strip steak': {'unit_cost': 0.9, 'unit': 'oz'},
                            'filet mignon': {'unit_cost': 1.15, 'unit': 'oz'},
                            'branzino whole': {'unit_cost': 8.5, 'unit': 'each'},
                            'gulf shrimp': {'unit_cost': 0.8, 'unit': 'oz'},
                            'andouille sausage': {'unit_cost': 0.55, 'unit': 'oz'},
                            'crawfish tail': {'unit_cost': 1.1, 'unit': 'oz'},
                            'crab roux base': {'unit_cost': 0.45, 'unit': 'oz'},
                            'okra': {'unit_cost': 0.25, 'unit': 'oz'},
                            'cavatappi pasta': {'unit_cost': 0.18, 'unit': 'oz'},
                            'dry spaghetti': {'unit_cost': 0.14, 'unit': 'oz'},
                            'pecorino romano': {'unit_cost': 0.85, 'unit': 'oz'},
                            'parmesan': {'unit_cost': 0.85, 'unit': 'oz'},
                            'heavy cream': {'unit_cost': 0.22, 'unit': 'oz'},
                            'butter': {'unit_cost': 0.3, 'unit': 'oz'},
                            'romaine heart': {'unit_cost': 0.9, 'unit': 'each'},
                            'iceberg wedge': {'unit_cost': 0.75, 'unit': 'each'},
                            'blue cheese': {'unit_cost': 0.7, 'unit': 'oz'},
                            'bacon': {'unit_cost': 0.55, 'unit': 'oz'},
                            'baby spinach': {'unit_cost': 0.35, 'unit': 'oz'},
                            'russet potato': {'unit_cost': 0.1, 'unit': 'oz'},
                            'black truffle oil': {'unit_cost': 1.2, 'unit': 'tbsp'},
                            'tomato': {'unit_cost': 0.2, 'unit': 'oz'},
                            'rice': {'unit_cost': 0.08, 'unit': 'oz'},
                            'croutons': {'unit_cost': 0.25, 'unit': 'oz'},
                            'anchovy': {'unit_cost': 0.9, 'unit': 'oz'},
                            'garlic': {'unit_cost': 0.35, 'unit': 'oz'},
                            'bourbon': {'unit_cost': 1.1, 'unit': 'oz'},
                            'vodka': {'unit_cost': 0.8, 'unit': 'oz'},
                            'espresso': {'unit_cost': 0.4, 'unit': 'oz'},
                            'coffee liqueur': {'unit_cost': 0.7, 'unit': 'oz'},
                            'simple syrup': {'unit_cost': 0.1, 'unit': 'oz'},
                            'bitters': {'unit_cost': 2.0, 'unit': 'oz'},
                            'brioche bread': {'unit_cost': 0.4, 'unit': 'oz'},
                            'egg': {'unit_cost': 0.3, 'unit': 'each'},
                            'vanilla bean': {'unit_cost': 1.5, 'unit': 'each'}}}


def list_dishes():
    """Return every dish with no cost/ingredient detail."""
    return [
        {
            "id": d["id"],
            "name": d["name"],
            "category": d["category"],
            "menu_price": d["menu_price"],
            "description": d["description"],
        }
        for d in MENU["dishes"]
    ]


def _select_dishes(keys):
    """Resolve a list of dish names or ids to dish dicts (order preserved).

    If keys is falsy, return all dishes.
    """
    if not keys:
        return list(MENU["dishes"])
    wanted = [str(k).strip().lower() for k in keys]
    selected = []
    for k in wanted:
        for d in MENU["dishes"]:
            if d["name"].lower() == k or d["id"].lower() == k:
                selected.append(d)
                break
    return selected


def decompose_dishes(dishes=None):
    """Map each requested dish name to its ingredient list."""
    result = {}
    for d in _select_dishes(dishes):
        result[d["name"]] = [
            {"ingredient": i["ingredient"], "qty": i["qty"], "unit": i["unit"]}
            for i in d["ingredients"]
        ]
    return result


def price_ingredients(ingredients=None):
    """Return unit costs for the requested ingredients (all if omitted)."""
    costs = MENU["ingredient_costs"]
    if not ingredients:
        return {name: dict(info) for name, info in costs.items()}
    result = {}
    for name in ingredients:
        info = costs.get(name)
        if info is not None:
            result[name] = dict(info)
    return result


def analyze_menu():
    """Deterministically score every dish and rank best value first.

    food_cost      = sum(qty * unit_cost) over the dish's ingredients
    markup_multiple = menu_price / food_cost   (lower = better value)
    food_cost_pct   = food_cost / menu_price * 100
    """
    costs = MENU["ingredient_costs"]
    scored = []
    errors = []
    for d in MENU["dishes"]:
        food_cost = 0.0
        ok = True
        for i in d["ingredients"]:
            info = costs.get(i["ingredient"])
            if info is None:
                errors.append(
                    "Missing cost for ingredient '%s' in dish '%s'"
                    % (i["ingredient"], d["name"])
                )
                ok = False
                continue
            food_cost += i["qty"] * info["unit_cost"]
        if not ok or food_cost <= 0:
            continue
        scored.append({
            "name": d["name"],
            "menu_price": d["menu_price"],
            "food_cost": round(food_cost, 2),
            "markup_multiple": round(d["menu_price"] / food_cost, 2),
            "food_cost_pct": round(food_cost / d["menu_price"] * 100, 1),
        })
    scored.sort(key=lambda r: r["markup_multiple"])
    out = {"dishes": scored}
    if errors:
        out["errors"] = errors
    return out


TOOLS = [
    {
        "name": "list_dishes",
        "description": (
            "List every dish on Hal's menu with id, name, category, "
            "menu_price, and description. No costs or ingredients."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        },
    },
    {
        "name": "decompose_dishes",
        "description": (
            "Break dishes down into their ingredients (ingredient, qty, "
            "unit). Pass a list of dish names or ids, or omit to get all."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "dishes": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Dish names or ids; omit/empty for all.",
                }
            },
            "additionalProperties": False,
        },
    },
    {
        "name": "price_ingredients",
        "description": (
            "Return wholesale unit_cost and unit for ingredients. Pass a "
            "list of ingredient names, or omit to get all."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "ingredients": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Ingredient names; omit/empty for all.",
                }
            },
            "additionalProperties": False,
        },
    },
    {
        "name": "analyze_menu",
        "description": (
            "Deterministically compute food_cost, markup_multiple, and "
            "food_cost_pct for every dish, ranked best value (lowest "
            "markup_multiple) first."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        },
    },
]


def dispatch_tool(name, arguments):
    """Call the named tool with its arguments; raise KeyError if unknown."""
    if name == "list_dishes":
        return list_dishes()
    if name == "decompose_dishes":
        return decompose_dishes(arguments.get("dishes"))
    if name == "price_ingredients":
        return price_ingredients(arguments.get("ingredients"))
    if name == "analyze_menu":
        return analyze_menu()
    raise KeyError(name)


def make_result(id_, result):
    return {"jsonrpc": "2.0", "id": id_, "result": result}


def make_error(id_, code, message):
    return {"jsonrpc": "2.0", "id": id_, "error": {"code": code, "message": message}}


def handle_message(msg):
    """Handle one parsed JSON-RPC message; return a response dict or None."""
    method = msg.get("method")
    msg_id = msg.get("id")
    params = msg.get("params") or {}

    # Notifications (no id) never get a response.
    if msg_id is None:
        return None

    if method == "initialize":
        protocol = params.get("protocolVersion", "2025-06-18")
        return make_result(msg_id, {
            "protocolVersion": protocol,
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "dining-roi", "version": "1.0.0"},
        })

    if method == "tools/list":
        return make_result(msg_id, {"tools": TOOLS})

    if method == "tools/call":
        name = params.get("name")
        arguments = params.get("arguments") or {}
        try:
            result = dispatch_tool(name, arguments)
        except KeyError:
            return make_result(msg_id, {
                "content": [{"type": "text", "text": "Unknown tool: %s" % name}],
                "isError": True,
            })
        return make_result(msg_id, {
            "content": [{"type": "text", "text": json.dumps(result)}]
        })

    if method == "resources/list":
        return make_result(msg_id, {"resources": []})

    if method == "prompts/list":
        return make_result(msg_id, {"prompts": []})

    if method == "ping":
        return make_result(msg_id, {})

    return make_error(msg_id, -32601, "Method not found")


def main():
    """Read newline-delimited JSON-RPC from stdin; write responses to stdout."""
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except Exception:
            # Unparseable line: no id available, so we cannot respond per spec.
            continue
        try:
            response = handle_message(msg)
        except Exception as exc:
            msg_id = msg.get("id") if isinstance(msg, dict) else None
            if msg_id is not None:
                response = make_error(msg_id, -32603, "Internal error: %s" % exc)
            else:
                response = None
        if response is not None:
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
