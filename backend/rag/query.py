# from rag.qa import answer_question

# print("✅ RAG Tutor ready.")
# print("Type your question below (type 'exit' to quit):\n")

# while True:
#     question = input("> ").strip()

#     if question.lower() in ("exit", "quit"):
#         print("Goodbye!")
#         break

#     answer, docs = answer_question(question, k=4, temperature=0.2)

#     print("\n🧠 Answer:\n")
#     print(answer)

#     print("\n📌 Sources:\n")
#     for i, d in enumerate(docs, start=1):
#         source = d.metadata.get("source", "unknown")
#         page = d.metadata.get("page", "?")
#         print(f"{i}) {source} (page {page})")

#     print("\n" + "=" * 60 + "\n")



from rag.qa import answer_question

print("✅ RAG Tutor ready.")
print("Type your question below (type 'exit' to quit):\n")

while True:
    question = input("> ").strip()

    if question.lower() in ("exit", "quit"):
        print("Goodbye!")
        break

    answer, docs = answer_question(question, k=4)

    print("\n📌 TOP MATCH (from PDF):\n")
    print(answer[:1200])
    print("\n" + "-" * 60)

    print("\n📚 SOURCES:\n")
    for i, doc in enumerate(docs, start=1):
        source = doc.metadata.get("source", "unknown")
        page = doc.metadata.get("page", "unknown")
        print(f"{i}) {source} (page {page})")

    print("\n")
