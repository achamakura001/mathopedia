from app import db
from app.models import Question

def seed_sample_questions():
    """Seed the database with sample questions for all grades"""
    
    sample_questions = [
        # Grade 1 Questions
        {
            'grade_level': '1',
            'complexity': 'easy',
            'topic': 'Addition',
            'question_text': 'What is 2 + 3?',
            'correct_answer': '5',
            'explanation': 'When we add 2 and 3, we count 2 items and then 3 more items. 2 + 3 = 5.'
        },
        {
            'grade_level': '1',
            'complexity': 'easy',
            'topic': 'Subtraction',
            'question_text': 'What is 5 - 2?',
            'correct_answer': '3',
            'explanation': 'When we subtract 2 from 5, we take away 2 items from 5 items. 5 - 2 = 3.'
        },
        {
            'grade_level': '1',
            'complexity': 'medium',
            'topic': 'Addition',
            'question_text': 'What is 7 + 4?',
            'correct_answer': '11',
            'explanation': 'To add 7 + 4, we can count up from 7: 8, 9, 10, 11. So 7 + 4 = 11.'
        },
        
        # Grade 2 Questions
        {
            'grade_level': '2',
            'complexity': 'easy',
            'topic': 'Addition',
            'question_text': 'What is 15 + 23?',
            'correct_answer': '38',
            'explanation': 'To add 15 + 23, we add the ones: 5 + 3 = 8, then the tens: 1 + 2 = 3. So 15 + 23 = 38.'
        },
        {
            'grade_level': '2',
            'complexity': 'medium',
            'topic': 'Multiplication',
            'question_text': 'What is 3 × 4?',
            'correct_answer': '12',
            'explanation': '3 × 4 means 3 groups of 4. We can count: 4 + 4 + 4 = 12.'
        },
        
        # Grade 3 Questions
        {
            'grade_level': '3',
            'complexity': 'easy',
            'topic': 'Multiplication',
            'question_text': 'What is 6 × 7?',
            'correct_answer': '42',
            'explanation': '6 × 7 = 42. This is a multiplication fact that can be memorized or calculated as 6 + 6 + 6 + 6 + 6 + 6 + 6.'
        },
        {
            'grade_level': '3',
            'complexity': 'medium',
            'topic': 'Division',
            'question_text': 'What is 24 ÷ 6?',
            'correct_answer': '4',
            'explanation': '24 ÷ 6 = 4 because 6 × 4 = 24. We can think: how many groups of 6 are in 24?'
        },
        
        # Grade 4 Questions
        {
            'grade_level': '4',
            'complexity': 'easy',
            'topic': 'Fractions',
            'question_text': 'What is 1/2 + 1/4?',
            'correct_answer': '3/4',
            'explanation': 'To add fractions, we need a common denominator. 1/2 = 2/4, so 2/4 + 1/4 = 3/4.'
        },
        {
            'grade_level': '4',
            'complexity': 'medium',
            'topic': 'Decimals',
            'question_text': 'What is 3.5 + 2.7?',
            'correct_answer': '6.2',
            'explanation': 'Line up the decimal points: 3.5 + 2.7 = 6.2. Add 5 + 7 = 12 (write 2, carry 1), then 3 + 2 + 1 = 6.'
        },
        
        # Grade 5 Questions
        {
            'grade_level': '5',
            'complexity': 'medium',
            'topic': 'Fractions',
            'question_text': 'What is 2/3 × 3/4?',
            'correct_answer': '6/12 or 1/2',
            'explanation': 'To multiply fractions: (2 × 3)/(3 × 4) = 6/12 = 1/2 when simplified.'
        },
        {
            'grade_level': '5',
            'complexity': 'hard',
            'topic': 'Percentages',
            'question_text': 'What is 25% of 80?',
            'correct_answer': '20',
            'explanation': '25% = 25/100 = 1/4. So 25% of 80 = 80 ÷ 4 = 20.'
        },
        
        # Grade 6 Questions
        {
            'grade_level': '6',
            'complexity': 'medium',
            'topic': 'Ratios',
            'question_text': 'If the ratio of boys to girls is 3:2 and there are 15 boys, how many girls are there?',
            'correct_answer': '10',
            'explanation': 'If boys:girls = 3:2, then for every 3 boys there are 2 girls. 15 boys ÷ 3 = 5 groups, so 5 × 2 = 10 girls.'
        },
        {
            'grade_level': '6',
            'complexity': 'hard',
            'topic': 'Integers',
            'question_text': 'What is (-5) + 8?',
            'correct_answer': '3',
            'explanation': 'When adding a positive to a negative, subtract the smaller absolute value from the larger: 8 - 5 = 3.'
        },
        
        # Grade 7 Questions
        {
            'grade_level': '7',
            'complexity': 'medium',
            'topic': 'Algebra',
            'question_text': 'Solve for x: 2x + 5 = 13',
            'correct_answer': '4',
            'explanation': 'Subtract 5 from both sides: 2x = 8. Divide both sides by 2: x = 4.'
        },
        {
            'grade_level': '7',
            'complexity': 'hard',
            'topic': 'Geometry',
            'question_text': 'What is the area of a circle with radius 3? (Use π ≈ 3.14)',
            'correct_answer': '28.26',
            'explanation': 'Area = πr² = 3.14 × 3² = 3.14 × 9 = 28.26 square units.'
        },
        
        # Grade 8 Questions
        {
            'grade_level': '8',
            'complexity': 'medium',
            'topic': 'Linear Equations',
            'question_text': 'What is the slope of the line y = 3x + 2?',
            'correct_answer': '3',
            'explanation': 'In the slope-intercept form y = mx + b, m is the slope. Here, m = 3.'
        },
        {
            'grade_level': '8',
            'complexity': 'hard',
            'topic': 'Pythagorean Theorem',
            'question_text': 'In a right triangle with legs 3 and 4, what is the hypotenuse?',
            'correct_answer': '5',
            'explanation': 'Using the Pythagorean theorem: c² = a² + b² = 3² + 4² = 9 + 16 = 25, so c = 5.'
        },
        
        # Grade 9 Questions
        {
            'grade_level': '9',
            'complexity': 'medium',
            'topic': 'Quadratic Equations',
            'question_text': 'Solve: x² - 5x + 6 = 0',
            'correct_answer': 'x = 2 or x = 3',
            'explanation': 'Factor: (x - 2)(x - 3) = 0. So x = 2 or x = 3.'
        },
        {
            'grade_level': '9',
            'complexity': 'hard',
            'topic': 'Functions',
            'question_text': 'If f(x) = 2x + 1, what is f(5)?',
            'correct_answer': '11',
            'explanation': 'Substitute x = 5 into f(x) = 2x + 1: f(5) = 2(5) + 1 = 10 + 1 = 11.'
        },
        
        # Grade 10 Questions
        {
            'grade_level': '10',
            'complexity': 'medium',
            'topic': 'Trigonometry',
            'question_text': 'What is sin(30°)?',
            'correct_answer': '0.5 or 1/2',
            'explanation': 'sin(30°) = 1/2 = 0.5. This is a standard trigonometric value.'
        },
        {
            'grade_level': '10',
            'complexity': 'hard',
            'topic': 'Logarithms',
            'question_text': 'What is log₂(8)?',
            'correct_answer': '3',
            'explanation': 'log₂(8) = 3 because 2³ = 8.'
        },
        
        # Grade 11 Questions
        {
            'grade_level': '11',
            'complexity': 'medium',
            'topic': 'Polynomials',
            'question_text': 'Expand: (x + 2)(x + 3)',
            'correct_answer': 'x² + 5x + 6',
            'explanation': 'Use FOIL: (x + 2)(x + 3) = x² + 3x + 2x + 6 = x² + 5x + 6.'
        },
        {
            'grade_level': '11',
            'complexity': 'hard',
            'topic': 'Sequences',
            'question_text': 'What is the 10th term of the arithmetic sequence 2, 5, 8, 11, ...?',
            'correct_answer': '29',
            'explanation': 'First term a₁ = 2, common difference d = 3. The nth term is aₙ = a₁ + (n-1)d = 2 + (10-1)×3 = 2 + 27 = 29.'
        },
        
        # Grade 12 Questions
        {
            'grade_level': '12',
            'complexity': 'medium',
            'topic': 'Calculus',
            'question_text': 'What is the derivative of x²?',
            'correct_answer': '2x',
            'explanation': 'Using the power rule: d/dx(xⁿ) = nxⁿ⁻¹, so d/dx(x²) = 2x¹ = 2x.'
        },
        {
            'grade_level': '12',
            'complexity': 'hard',
            'topic': 'Limits',
            'question_text': 'What is lim(x→0) (sin x)/x?',
            'correct_answer': '1',
            'explanation': 'This is a standard limit in calculus: lim(x→0) (sin x)/x = 1.'
        },
        
        # Advanced Math Questions with LaTeX
        {
            'grade_level': '11',
            'complexity': 'hard',
            'topic': 'Trigonometric Identities',
            'question_text': 'Verify the Product-to-Sum Identity:\n\\[\n\\sin A \\cos B = \\frac{1}{2} [\\sin(A + B) + \\sin(A - B)]\n\\]\nby expressing \\(\\sin A \\cos B\\) as a sum of sines using known identities',
            'correct_answer': 'Using sum and difference formulas for sine',
            'explanation': 'Using the sum and difference formulas:\n\\(\\sin(A + B) = \\sin A \\cos B + \\cos A \\sin B\\)\n\\(\\sin(A - B) = \\sin A \\cos B - \\cos A \\sin B\\)\nAdding these equations:\n\\(\\sin(A + B) + \\sin(A - B) = 2\\sin A \\cos B\\)\nTherefore: \\(\\sin A \\cos B = \\frac{1}{2}[\\sin(A + B) + \\sin(A - B)]\\)'
        },
        {
            'grade_level': '10',
            'complexity': 'medium',
            'topic': 'Trigonometric Functions',
            'question_text': 'Find the angle \\(\\theta\\) where \\(0° ≤ \\theta ≤ 360°\\) if \\(\\sin \\theta = \\frac{\\sqrt{3}}{2}\\)',
            'correct_answer': '60°, 120°',
            'explanation': 'The equation \\(\\sin \\theta = \\frac{\\sqrt{3}}{2}\\) has solutions in the first and second quadrants.\nIn the first quadrant: \\(\\theta = 60°\\)\nIn the second quadrant: \\(\\theta = 180° - 60° = 120°\\)'
        },
        {
            'grade_level': '12',
            'complexity': 'hard',
            'topic': 'Calculus',
            'question_text': 'Find the derivative of \\(f(x) = x^2 \\sin(x)\\) using the product rule',
            'correct_answer': '2x sin(x) + x² cos(x)',
            'explanation': 'Using the product rule: \\((uv)\\prime = u\\prime v + uv\\prime\\)\nLet \\(u = x^2\\) and \\(v = \\sin(x)\\)\nThen \\(u\\prime = 2x\\) and \\(v\\prime = \\cos(x)\\)\nSo \\(f\\prime(x) = 2x \\cdot \\sin(x) + x^2 \\cdot \\cos(x) = 2x\\sin(x) + x^2\\cos(x)\\)'
        },
        {
            'grade_level': '9',
            'complexity': 'medium',
            'topic': 'Quadratic Equations',
            'question_text': 'Solve the quadratic equation \\(x^2 - 5x + 6 = 0\\) using the quadratic formula',
            'correct_answer': 'x = 2, x = 3',
            'explanation': 'Using the quadratic formula: \\(x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}\\)\nFor \\(x^2 - 5x + 6 = 0\\), we have \\(a = 1\\), \\(b = -5\\), \\(c = 6\\)\n\\(x = \\frac{5 \\pm \\sqrt{25 - 24}}{2} = \\frac{5 \\pm 1}{2}\\)\nSo \\(x = 3\\) or \\(x = 2\\)'
        },
        {
            'grade_level': '11',
            'complexity': 'hard',
            'topic': 'Logarithms',
            'question_text': 'Simplify: \\(\\log_2(8) + \\log_2(4) - \\log_2(16)\\)',
            'correct_answer': '1',
            'explanation': 'Using logarithm properties:\n\\(\\log_2(8) = \\log_2(2^3) = 3\\)\n\\(\\log_2(4) = \\log_2(2^2) = 2\\)\n\\(\\log_2(16) = \\log_2(2^4) = 4\\)\nTherefore: \\(3 + 2 - 4 = 1\\)'
        },
        {
            'grade_level': 'Competitive Exams',
            'complexity': 'hard',
            'topic': 'Complex Numbers',
            'question_text': 'Find the modulus of the complex number \\(z = 3 + 4i\\)',
            'correct_answer': '5',
            'explanation': 'The modulus of a complex number \\(z = a + bi\\) is given by:\n\\(|z| = \\sqrt{a^2 + b^2}\\)\nFor \\(z = 3 + 4i\\):\n\\(|z| = \\sqrt{3^2 + 4^2} = \\sqrt{9 + 16} = \\sqrt{25} = 5\\)'
        },
        {
            'grade_level': 'Competitive Exams',
            'complexity': 'hard',
            'topic': 'Integration',
            'question_text': 'Evaluate the integral \\(\\int_0^{\\pi/2} \\sin(x) \\, dx\\)',
            'correct_answer': '1',
            'explanation': 'To evaluate \\(\\int \\sin(x) \\, dx\\), we use the antiderivative:\n\\(\\int \\sin(x) \\, dx = -\\cos(x) + C\\)\nEvaluating from 0 to \\(\\pi/2\\):\n\\([-\\cos(x)]_0^{\\pi/2} = -\\cos(\\pi/2) - (-\\cos(0)) = 0 - (-1) = 1\\)'
        }
    ]
    
    # Clear existing questions (optional - comment out in production)
    # Question.query.delete()
    
    # Add all sample questions
    for question_data in sample_questions:
        # Check if question already exists
        existing = Question.query.filter_by(
            grade_level=question_data['grade_level'],
            question_text=question_data['question_text']
        ).first()
        
        if not existing:
            question = Question(**question_data)
            db.session.add(question)
    
    try:
        db.session.commit()
        print(f"Successfully seeded {len(sample_questions)} sample questions!")
    except Exception as e:
        db.session.rollback()
        print(f"Error seeding questions: {e}")
        raise
