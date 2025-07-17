import React, { useState, useEffect } from 'react';
import { ArrowRight, Users, Brain, Target, Sparkles, Instagram, Twitter, Linkedin, MessageSquare, Loader, CheckCircle, AlertCircle } from 'lucide-react';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { personaPulseAPI } from '../services/api';

const Home = () => {
  const [formData, setFormData] = useState({
    instagram: '',
    twitter: '',
    linkedin: '',
    reddit: ''
  });
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [showForm, setShowForm] = useState(false);

  const features = [
    {
      icon: Users,
      title: "Social Analysis",
      description: "Analyzes your social media presence across multiple platforms to understand your interests and behavior patterns.",
      delay: "animate-fadeIn"
    },
    {
      icon: Brain,
      title: "Personality Scoring",
      description: "Advanced OCEAN personality analysis to understand your openness, conscientiousness, extraversion, agreeableness, and neuroticism.",
      delay: "animate-fadeInDelay"
    },
    {
      icon: Target,
      title: "Smart Matching",
      description: "Intelligent keyword and personality alignment to match you with events that resonate with your interests.",
      delay: "animate-fadeInDelay2"
    },
    {
      icon: Sparkles,
      title: "Curated Dashboard",
      description: "Personalized event recommendations delivered through a beautiful, intuitive dashboard tailored to your preferences.",
      delay: "animate-fadeInDelay3"
    }
  ];

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Check if at least one social media ID is provided
    const hasAtLeastOne = Object.values(formData).some(value => value.trim() !== '');
    if (!hasAtLeastOne) {
      setError('Please provide at least one social media ID');
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);

    try {
      // Filter out empty values
      const socialMediaIds = Object.fromEntries(
        Object.entries(formData).filter(([key, value]) => value.trim() !== '')
      );

      const response = await personaPulseAPI.createUser(socialMediaIds);
      setResult(response);
      
      // Reset form
      setFormData({
        instagram: '',
        twitter: '',
        linkedin: '',
        reddit: ''
      });
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  const resetForm = () => {
    setFormData({
      instagram: '',
      twitter: '',
      linkedin: '',
      reddit: ''
    });
    setResult(null);
    setError('');
    setShowForm(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-muted to-background">
      {/* Floating Background Elements */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-4 -left-4 w-72 h-72 bg-primary/10 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-float"></div>
        <div className="absolute -bottom-8 -right-4 w-72 h-72 bg-accent/10 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-float-delayed"></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-gradient-to-r from-primary/5 to-accent/5 rounded-full mix-blend-multiply filter blur-2xl opacity-60 animate-pulse-custom"></div>
      </div>

      {/* Hero Section */}
      <section id="home" className="relative pt-32 pb-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto text-center">
          <div className="animate-fadeIn">
            <h1 className="text-5xl md:text-7xl font-bold mb-6">
              <span className="bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
                PersonaPulse
              </span>
            </h1>
            <p className="text-xl md:text-2xl text-muted-foreground mb-8 max-w-3xl mx-auto">
              Discover Events That Match Your Personality
            </p>
            <p className="text-lg text-muted-foreground mb-12 max-w-2xl mx-auto">
              Our AI-powered platform analyzes your social media presence and personality to suggest perfectly matched events tailored just for you.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
              <Button 
                size="lg" 
                className="animate-bounce-subtle"
                onClick={() => setShowForm(true)}
              >
                Get Started
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
              <Button variant="outline" size="lg">
                Learn More
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Powerful Features
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Discover how PersonaPulse transforms your social media data into personalized event recommendations
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <Card key={index} className={`${feature.delay} group`}>
                <CardHeader className="text-center">
                  <div className="mx-auto mb-4 w-12 h-12 bg-gradient-to-r from-primary to-accent rounded-lg flex items-center justify-center group-hover:rotate-12 transition-transform duration-300">
                    <feature.icon className="h-6 w-6 text-white" />
                  </div>
                  <CardTitle className="text-xl">{feature.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription className="text-center">
                    {feature.description}
                  </CardDescription>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* User Analysis Form Modal */}
      {showForm && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-bold">Start Your Personality Analysis</h2>
                <Button variant="ghost" size="icon" onClick={resetForm}>
                  <ArrowRight className="h-5 w-5 rotate-45" />
                </Button>
              </div>

              {!result ? (
                <form onSubmit={handleSubmit} className="space-y-6">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <label className="flex items-center text-sm font-medium">
                        <Instagram className="h-4 w-4 mr-2 text-pink-500" />
                        Instagram Username
                      </label>
                      <input
                        type="text"
                        name="instagram"
                        value={formData.instagram}
                        onChange={handleInputChange}
                        placeholder="@username"
                        className="w-full px-3 py-2 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
                      />
                    </div>

                    <div className="space-y-2">
                      <label className="flex items-center text-sm font-medium">
                        <Twitter className="h-4 w-4 mr-2 text-blue-500" />
                        Twitter Username
                      </label>
                      <input
                        type="text"
                        name="twitter"
                        value={formData.twitter}
                        onChange={handleInputChange}
                        placeholder="@username"
                        className="w-full px-3 py-2 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
                      />
                    </div>

                    <div className="space-y-2">
                      <label className="flex items-center text-sm font-medium">
                        <Linkedin className="h-4 w-4 mr-2 text-blue-600" />
                        LinkedIn Profile
                      </label>
                      <input
                        type="text"
                        name="linkedin"
                        value={formData.linkedin}
                        onChange={handleInputChange}
                        placeholder="username or profile URL"
                        className="w-full px-3 py-2 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
                      />
                    </div>

                    <div className="space-y-2">
                      <label className="flex items-center text-sm font-medium">
                        <MessageSquare className="h-4 w-4 mr-2 text-orange-500" />
                        Reddit Username
                      </label>
                      <input
                        type="text"
                        name="reddit"
                        value={formData.reddit}
                        onChange={handleInputChange}
                        placeholder="u/username"
                        className="w-full px-3 py-2 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
                      />
                    </div>
                  </div>

                  {error && (
                    <div className="flex items-center p-3 text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg">
                      <AlertCircle className="h-4 w-4 mr-2" />
                      {error}
                    </div>
                  )}

                  <div className="flex gap-3">
                    <Button
                      type="submit"
                      disabled={loading}
                      className="flex-1"
                    >
                      {loading ? (
                        <>
                          <Loader className="h-4 w-4 mr-2 animate-spin" />
                          Analyzing...
                        </>
                      ) : (
                        'Analyze My Personality'
                      )}
                    </Button>
                    <Button variant="outline" onClick={resetForm}>
                      Cancel
                    </Button>
                  </div>
                </form>
              ) : (
                <div className="text-center space-y-4">
                  <div className="flex items-center justify-center w-16 h-16 mx-auto bg-green-100 rounded-full">
                    <CheckCircle className="h-8 w-8 text-green-600" />
                  </div>
                  <h3 className="text-xl font-semibold">Analysis Complete!</h3>
                  <p className="text-muted-foreground">
                    Your personality profile has been created successfully.
                  </p>
                  {result.data && (
                    <div className="bg-muted p-4 rounded-lg text-left">
                      <p className="text-sm font-medium">User ID: {result.data.unique_id}</p>
                      <p className="text-sm text-muted-foreground mt-1">
                        Your personalized event recommendations will be available shortly.
                      </p>
                    </div>
                  )}
                  <Button onClick={resetForm} className="w-full">
                    Create Another Profile
                  </Button>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Call to Action Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-r from-primary/5 to-accent/5">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-6">
            Ready to Find Your Perfect Events?
          </h2>
          <p className="text-lg text-muted-foreground mb-8 max-w-2xl mx-auto">
            Join thousands of users who have discovered events that truly match their personality and interests.
          </p>
          <Button 
            size="lg" 
            className="animate-bounce-subtle"
            onClick={() => setShowForm(true)}
          >
            Start Your Journey
            <ArrowRight className="ml-2 h-5 w-5" />
          </Button>
        </div>
      </section>
    </div>
  );
};

export default Home;
