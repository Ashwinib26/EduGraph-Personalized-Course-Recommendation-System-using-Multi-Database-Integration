from neo4j import GraphDatabase

try:
    uri = "bolt://localhost:7687"
    user = "neo4j"
    password = "neo4j"   # replace with your password

    neo4j_driver = GraphDatabase.driver(uri, auth=(user, password))
    with neo4j_driver.session() as session:
        result = session.run("RETURN 1 AS ok").single()
        print("✅ Connected to Neo4j Desktop:", result["ok"])
except Exception as e:
    print("❌ Neo4j connection failed:", e)
