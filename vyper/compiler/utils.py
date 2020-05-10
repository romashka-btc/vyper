def build_gas_estimates(lll_nodes):
    gas_estimates = {}

    # Extract the stuff inside the LLL bracket
    if lll_nodes.value == "seq":
        if len(lll_nodes.args) > 0 and lll_nodes.args[-1].value == "return":
            lll_nodes = lll_nodes.args[-1].args[1].args[0]

    assert lll_nodes.value == "seq"
    for arg in lll_nodes.args:
        if arg.func_name is not None:
            gas_estimates[arg.func_name] = arg.total_gas

    return gas_estimates


def expand_source_map(compressed_map):
    source_map = [_expand_row(i) if i else None for i in compressed_map.split(";")[:-1]]

    for i, value in enumerate(source_map[1:], 1):
        if value is None:
            source_map[i] = source_map[i - 1][:3] + [None]
            continue
        for x in range(3):
            if source_map[i][x] is None:
                source_map[i][x] = source_map[i - 1][x]

    return source_map


def _expand_row(row):
    result = [None] * 4
    for i, value in enumerate(row.split(":")):
        if value:
            result[i] = value if i == 3 else int(value)
    return result
