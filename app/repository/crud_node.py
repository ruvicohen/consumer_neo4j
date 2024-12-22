from dataclasses import asdict
from operator import itemgetter
from typing import Any, Dict, TypeVar, List
from returns.maybe import Maybe, Nothing
from toolz import curry
import toolz as t
from app.db.database_neo4j import driver

T = TypeVar('T')

@curry
def create_node(node_type: str, object: T) -> Maybe:
    object_as_dict = asdict(object)
    if any(value is None for value in object_as_dict.values()):
        print(f"Skipping node creation due to null values: {object_as_dict}")
        return Nothing
    with driver.session() as session:
        query = f"""
        MERGE (n:{node_type} {{ {', '.join([f'{k}: ${k}' for k in object_as_dict])} }})
        RETURN n"""

        params = object_as_dict

        res = session.run(query, params).single()

        return (
            Maybe.from_optional(res.get("n")).map(lambda n: {
                "id": n.element_id.split(":")[2],
                "properties": dict(n)
            })
        )

@curry
def create_node1(node_type: str, object: T) -> Maybe:
    object_as_dict = asdict(object)
    if any(value is None for value in object_as_dict.values()):
        print(f"Skipping node creation due to null values: {object_as_dict}")
        return Nothing
    with driver.session() as session:
        query = f"""
        CREATE (n:{node_type} {{ {', '.join([f'{k}: ${k}' for k in object_as_dict])} }})
        RETURN n"""

        params = object_as_dict

        res = session.run(query, params).single()

        return (
            Maybe.from_optional(res.get("n")).map(lambda n: {
                "id": n.element_id.split(":")[2],
                "properties": dict(n)
            })
        )

@curry
def get_all_nodes(node_type: str) -> List[T]:
    with driver.session() as session:
        query = f"""
        MATCH (n:{node_type})
        RETURN n
        """

        res = session.run(query).data()

        return t.pipe(
            res,
            t.partial(t.pluck, "n"),
            list
        )

@curry
def get_node_by_id(node_type: str, node_id: int) -> List[T]:
    with driver.session() as session:
        query = f"""
        MATCH (n:{node_type})
        WHERE ID(n) = $node_id
        RETURN n
        """
        params = {"node_id": node_id}

        res = session.run(query, params).data()

        return t.pipe(
            res,
            t.partial(t.pluck, "n"),
            list
        )

@curry
def update_node(node_type: str, node_id: int, node: T) -> Maybe:
    if not get_node_by_id(node_type, node_id):
        return Maybe.from_optional({"error": f"{node_type} not found"})

    properties = asdict(node)
    with driver.session() as session:
        query = f"""
        MATCH (n:{node_type})
        WHERE ID(n) = $node_id
        SET {', '.join([f'n.{key} = ${key}' for key in properties])}
        RETURN n
        """
        params = {"node_id": node_id, **properties}
        res = session.run(query, params).single()
        return Maybe.from_optional(res.get("n")).map(lambda n: dict(n))

@curry
def delete_node(node_type: str, node_id: int) -> Dict[str, Any]:
    with driver.session() as session:
        query = f"""
        MATCH (n:{node_type})
        WHERE ID(n) = $node_id
        DETACH DELETE n
        RETURN COUNT(*) as deletedCount
        """
        params = {"node_id": node_id}
        res = session.run(query, params).single()["deletedCount"]
        return {"success": res > 0, "deletedCount": res}


@curry
def create_relationship(relationship_type: str,source_type: str,target_type: str,source_node_id: int, target_node_id: int,
                        relationship_props: Dict[str, Any] = None) -> Maybe:
    print(source_node_id)
    print(target_node_id)
    with driver.session() as session:
        print(1)
        props_clause = ""
        if relationship_props:
            props_clause = f"{{ {', '.join([f'{k}: ${k}' for k in relationship_props.keys()])} }}"
        query = f"""
            MATCH (s:{source_type}) WHERE id(s) = $source_node_id
            MATCH (t:{target_type}) WHERE id(t) = $target_node_id
            MERGE (s)-[r:{relationship_type} {props_clause}]->(t)
            RETURN r
            """
        print(2)
        params = {"source_node_id": source_node_id, "target_node_id": target_node_id, **(relationship_props or {})}
        print(3)
        res = session.run(query, params).single()
        print(4)
        return Maybe.from_optional(res).map(itemgetter('r')).map(lambda x: dict(x))

@curry
def update_relationship(relationship_type: str ,source_type: str,target_type: str,source_node_id: int, target_node_id: int,relationship_props):
    with driver.session() as session:
        props_clause = f"{{ {', '.join([f'{k}: ${k}' for k in relationship_props.keys()])} }}"
        query = f"""
            MATCH (s:{source_type}) WHERE id(s) = $source_node_id
            MATCH (t:{target_type}) WHERE id(t) = $target_node_id
            MERGE (s)-[r:{relationship_type} {props_clause}]->(t)
            RETURN r
            """
        params = {"source_node_id": source_node_id, "target_node_id": target_node_id, **(relationship_props or {})}
        res = session.run(query, params).single()
        return Maybe.from_optional(res).map(itemgetter('r')).map(lambda x: dict(x))


@curry
def delete_relationship(relationship_type: str, source_type: str, target_type: str,
                        source_node_id: int, target_node_id: int) -> Maybe:
    with driver.session() as session:
        query = f"""
        MATCH (s:{source_type})-[r:{relationship_type}]->(t:{target_type})
        WHERE id(s) = $source_node_id AND id(t) = $target_node_id
        DELETE r
        RETURN COUNT(r) AS deletedCount
        """

        params = {"source_node_id": source_node_id, "target_node_id": target_node_id}

        res = session.run(query, params).single()

        return Maybe.from_optional(res).map(lambda x: {"deletedCount": x["deletedCount"]})