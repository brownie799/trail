from app.services.retriever import RetrieverService

seed_docs = [
    {
        "title": "WHO Vaccine Safety",
        "source": "https://www.who.int",
        "content": "Vaccines undergo rigorous testing for safety and efficacy before approval by regulators.",
    },
    {
        "title": "NASA Climate Evidence",
        "source": "https://climate.nasa.gov",
        "content": "Scientific evidence shows Earth is warming, with trends measured across multiple independent datasets.",
    },
    {
        "title": "CDC Measles Guidance",
        "source": "https://www.cdc.gov",
        "content": "Measles is highly contagious and vaccination is the most effective prevention method.",
    },
]

if __name__ == "__main__":
    r = RetrieverService()
    for d in seed_docs:
        r.add_document(d["title"], d["source"], d["content"], tags=["seed"])
    print("Knowledge base initialized with seed documents.")
