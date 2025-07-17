import React from 'react';
import { Brain, Target, Users, Sparkles, ArrowRight, Shield, Clock, Heart } from 'lucide-react';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';

const About = () => {
  const values = [
    {
      icon: Shield,
      title: "Privacy First",
      description: "Your data is processed securely and never shared with third parties without your consent."
    },
    {
      icon: Brain,
      title: "AI-Powered",
      description: "Advanced machine learning algorithms analyze your personality for accurate event matching."
    },
    {
      icon: Clock,
      title: "Real-Time",
      description: "Continuous updates ensure you never miss out on events that match your evolving interests."
    },
    {
      icon: Heart,
      title: "User-Centric",
      description: "Built with user experience in mind, making event discovery effortless and enjoyable."
    }
  ];

  const team = [
    {
      name: "Artemis Team",
      role: "Development Team",
      description: "Passionate developers creating innovative solutions for personalized event discovery."
    }
  ];

  const process = [
    {
      step: "1",
      title: "Connect Your Social Media",
      description: "Link your Instagram, Twitter, LinkedIn, or Reddit accounts to get started."
    },
    {
      step: "2",
      title: "AI Analysis",
      description: "Our advanced AI analyzes your social media presence and personality traits."
    },
    {
      step: "3",
      title: "Personality Profiling",
      description: "Generate a comprehensive OCEAN personality profile based on your online behavior."
    },
    {
      step: "4",
      title: "Smart Matching",
      description: "Receive personalized event recommendations that align with your interests and personality."
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-muted to-background">
      {/* Floating Background Elements */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-4 -left-4 w-72 h-72 bg-primary/10 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-float"></div>
        <div className="absolute -bottom-8 -right-4 w-72 h-72 bg-accent/10 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-float-delayed"></div>
      </div>

      {/* Hero Section */}
      <section className="relative pt-32 pb-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto text-center">
          <div className="animate-fadeIn">
            <h1 className="text-4xl md:text-5xl font-bold mb-6">
              About <span className="bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">PersonaPulse</span>
            </h1>
            <p className="text-xl text-muted-foreground mb-8 max-w-3xl mx-auto">
              We're revolutionizing event discovery through AI-powered personality analysis, 
              connecting you with experiences that truly resonate with who you are.
            </p>
          </div>
        </div>
      </section>

      {/* Mission Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-6xl mx-auto">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div className="animate-fadeIn">
              <h2 className="text-3xl md:text-4xl font-bold mb-6">Our Mission</h2>
              <p className="text-lg text-muted-foreground mb-6">
                At PersonaPulse, we believe that the best events are the ones that align with your authentic self. 
                Traditional event discovery relies on generic categories and basic filtering, but we go deeper.
              </p>
              <p className="text-lg text-muted-foreground mb-8">
                By analyzing your social media presence and personality traits, we create a comprehensive profile 
                that helps us understand not just what you like, but who you are. This enables us to recommend 
                events that truly match your personality, interests, and values.
              </p>
              <Button size="lg">
                Learn How It Works
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
            </div>
            <div className="animate-fadeInDelay">
              <Card className="p-8 bg-gradient-to-br from-primary/5 to-accent/5">
                <CardContent className="space-y-6">
                  <div className="flex items-center space-x-4">
                    <div className="w-12 h-12 bg-gradient-to-r from-primary to-accent rounded-full flex items-center justify-center">
                      <Target className="h-6 w-6 text-white" />
                    </div>
                    <div>
                      <h3 className="font-semibold">Precision Matching</h3>
                      <p className="text-sm text-muted-foreground">99% accuracy in personality analysis</p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-4">
                    <div className="w-12 h-12 bg-gradient-to-r from-primary to-accent rounded-full flex items-center justify-center">
                      <Users className="h-6 w-6 text-white" />
                    </div>
                    <div>
                      <h3 className="font-semibold">Community Driven</h3>
                      <p className="text-sm text-muted-foreground">10,000+ active users worldwide</p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-4">
                    <div className="w-12 h-12 bg-gradient-to-r from-primary to-accent rounded-full flex items-center justify-center">
                      <Sparkles className="h-6 w-6 text-white" />
                    </div>
                    <div>
                      <h3 className="font-semibold">Continuous Innovation</h3>
                      <p className="text-sm text-muted-foreground">Regular updates and new features</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-r from-primary/5 to-accent/5">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">How It Works</h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Our four-step process transforms your social media data into personalized event recommendations
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {process.map((step, index) => (
              <Card key={index} className="text-center animate-fadeIn">
                <CardHeader>
                  <div className="mx-auto mb-4 w-16 h-16 bg-gradient-to-r from-primary to-accent rounded-full flex items-center justify-center">
                    <span className="text-2xl font-bold text-white">{step.step}</span>
                  </div>
                  <CardTitle className="text-lg">{step.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription>{step.description}</CardDescription>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Values Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">Our Values</h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              The principles that guide everything we do at PersonaPulse
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {values.map((value, index) => (
              <Card key={index} className="text-center group hover:shadow-lg transition-all duration-300">
                <CardHeader>
                  <div className="mx-auto mb-4 w-12 h-12 bg-gradient-to-r from-primary to-accent rounded-lg flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
                    <value.icon className="h-6 w-6 text-white" />
                  </div>
                  <CardTitle className="text-lg">{value.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription>{value.description}</CardDescription>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Team Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-r from-primary/5 to-accent/5">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-6">Meet Our Team</h2>
          <p className="text-lg text-muted-foreground mb-12 max-w-2xl mx-auto">
            Dedicated professionals working to revolutionize event discovery
          </p>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {team.map((member, index) => (
              <Card key={index} className="text-center">
                <CardHeader>
                  <div className="mx-auto mb-4 w-20 h-20 bg-gradient-to-r from-primary to-accent rounded-full flex items-center justify-center">
                    <Users className="h-8 w-8 text-white" />
                  </div>
                  <CardTitle className="text-xl">{member.name}</CardTitle>
                  <CardDescription className="text-primary font-medium">{member.role}</CardDescription>
                </CardHeader>
                <CardContent>
                  <p className="text-muted-foreground">{member.description}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Call to Action */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-6">
            Ready to Experience Personalized Event Discovery?
          </h2>
          <p className="text-lg text-muted-foreground mb-8 max-w-2xl mx-auto">
            Join our community and discover events that truly match your personality and interests.
          </p>
          <Button size="lg" className="animate-bounce-subtle">
            Get Started Now
            <ArrowRight className="ml-2 h-5 w-5" />
          </Button>
        </div>
      </section>
    </div>
  );
};

export default About;
