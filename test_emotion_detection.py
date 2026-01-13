import unittest
from EmotionDetection import emotion_detector
import json

class TestEmotionDetector(unittest.TestCase):
    """Tests unitaires pour la fonction emotion_detector"""
    
    def test_joy_statement(self):
        """Test pour une déclaration de joie"""
        print("Test 1: 'Je suis content que cela soit arrivé'")
        result = emotion_detector("Je suis content que cela soit arrivé")
        print(f"Résultat: {json.dumps(result, indent=2)}")
        self.assertIsNotNone(result['dominant_emotion'])
        print(f"Émotion dominante: {result['dominant_emotion']}")
        print("="*60)
    
    def test_anger_statement(self):
        """Test pour une déclaration de colère"""
        print("\nTest 2: 'Je suis vraiment en colère à ce sujet'")
        result = emotion_detector("Je suis vraiment en colère à ce sujet")
        print(f"Résultat: {json.dumps(result, indent=2)}")
        self.assertIsNotNone(result['dominant_emotion'])
        print(f"Émotion dominante: {result['dominant_emotion']}")
        print("="*60)
    
    def test_disgust_statement(self):
        """Test pour une déclaration de dégoût"""
        print("\nTest 3: 'Je me sens dégoûté rien qu'en entendant parler de cela'")
        result = emotion_detector("Je me sens dégoûté rien qu'en entendant parler de cela")
        print(f"Résultat: {json.dumps(result, indent=2)}")
        self.assertIsNotNone(result['dominant_emotion'])
        print(f"Émotion dominante: {result['dominant_emotion']}")
        print("="*60)
    
    def test_sadness_statement(self):
        """Test pour une déclaration de tristesse"""
        print("\nTest 4: 'Je suis tellement triste à ce sujet'")
        result = emotion_detector("Je suis tellement triste à ce sujet")
        print(f"Résultat: {json.dumps(result, indent=2)}")
        self.assertIsNotNone(result['dominant_emotion'])
        print(f"Émotion dominante: {result['dominant_emotion']}")
        print("="*60)
    
    def test_fear_statement(self):
        """Test pour une déclaration de peur"""
        print("\nTest 5: 'J'ai vraiment peur que cela se produise'")
        result = emotion_detector("J'ai vraiment peur que cela se produise")
        print(f"Résultat: {json.dumps(result, indent=2)}")
        self.assertIsNotNone(result['dominant_emotion'])
        print(f"Émotion dominante: {result['dominant_emotion']}")
        print("="*60)

if __name__ == '__main__':
    print("=== DÉBUT DES TESTS UNITAIRES ===")
    print("Test du package EmotionDetection")
    print("="*60)
    
    # Exécuter les tests avec plus de détails
    suite = unittest.TestLoader().loadTestsFromTestCase(TestEmotionDetector)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "="*60)
    print("=== RÉSUMÉ DES TESTS ===")
    
    if result.wasSuccessful():
        print("✅ Tous les tests ont réussi !")
    else:
        print(f"❌ {len(result.failures)} test(s) ont échoué")
        print(f"   {len(result.errors)} test(s) ont des erreurs")