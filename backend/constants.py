"""Application-wide constant strings such as knowledge base content
and system prompts live in this module so they can be imported from
anywhere without causing circular dependencies.
"""

KNOWLEDGE_BASE = """
Basic knowledge about artificial intelligence:

1. AI Definition
Artificial Intelligence (AI) is a branch of computer science dedicated to creating machines capable of simulating human intelligence.

2. Machine Learning
Machine learning is a subset of AI that enables computers to learn from data without explicit programming.

3. Deep Learning
Deep learning is a branch of machine learning that uses multi-layer neural networks to learn data representations.

4. Natural Language Processing
NLP enables computers to understand, interpret, and generate human language.

5. Computer Vision
Computer vision enables machines to understand and process visual information.
"""

CODE_ANALYSIS_PROMPT = """
Please analyze the following code in terms of:

1. Code complexity analysis:
   - Time complexity
   - Space complexity
   - Code structure complexity

2. Completion assessment:
   - Functionality completeness
   - Error handling
   - Boundary case handling

3. Code quality analysis:
   - Code readability
   - Naming conventions
   - Comment completeness
   - Code reusability

4. Improvement suggestions:
   - Performance optimization suggestions
   - Code structure optimization suggestions
   - Security suggestions

Please provide a detailed analysis report.
""" 