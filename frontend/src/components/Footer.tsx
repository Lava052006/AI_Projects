import { motion } from "framer-motion";
import { Code2, Heart, Github, Twitter, Linkedin } from "lucide-react";

export default function Footer() {
  const socialLinks = [
    { icon: Github, href: "#", label: "GitHub" },
    { icon: Twitter, href: "#", label: "Twitter" },
    { icon: Linkedin, href: "#", label: "LinkedIn" },
  ];

  const footerLinks = [
    {
      title: "Product",
      links: [
        { name: "Demo", href: "/review" },
        { name: "Architecture", href: "/vision" },
        { name: "Features", href: "/#features" },
      ]
    },
    {
      title: "Resources",
      links: [
        { name: "Documentation", href: "#" },
        { name: "API Reference", href: "#" },
        { name: "Support", href: "#" },
      ]
    },
    {
      title: "Company",
      links: [
        { name: "About", href: "#" },
        { name: "Blog", href: "#" },
        { name: "Contact", href: "#" },
      ]
    }
  ];

  return (
    <footer className="bg-slate-900/60 border-t border-slate-700/50 backdrop-blur-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-8">
          {/* Enhanced Brand */}
          <div className="lg:col-span-2">
            <motion.div 
              whileHover={{ scale: 1.05 }}
              className="flex items-center space-x-3 mb-6"
            >
              <div className="w-10 h-10 bg-gradient-to-r from-primary-500 to-primary-600 rounded-xl flex items-center justify-center shadow-lg">
                <Code2 className="w-6 h-6 text-white" />
              </div>
              <span className="text-xl font-bold gradient-text">AI Mentor</span>
            </motion.div>
            
            <p className="text-gray-400 mb-8 max-w-md leading-relaxed">
              AI-powered code review tool that helps developers write better Python code. 
              Built with privacy and performance in mind.
            </p>
            
            <div className="flex items-center space-x-4">
              {socialLinks.map((social) => {
                const Icon = social.icon;
                return (
                  <motion.a
                    key={social.label}
                    href={social.href}
                    whileHover={{ scale: 1.1, y: -2 }}
                    whileTap={{ scale: 0.95 }}
                    className="w-12 h-12 bg-slate-800/80 hover:bg-gradient-to-r hover:from-primary-500/20 hover:to-primary-600/20 rounded-xl flex items-center justify-center text-gray-400 hover:text-primary-400 transition-all duration-300 border border-slate-700/50 hover:border-primary-500/30"
                    aria-label={social.label}
                  >
                    <Icon className="w-5 h-5" />
                  </motion.a>
                );
              })}
            </div>
          </div>

          {/* Enhanced Links */}
          {footerLinks.map((section, index) => (
            <motion.div
              key={section.title}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              viewport={{ once: true }}
            >
              <h3 className="text-white font-semibold mb-6 text-lg">{section.title}</h3>
              <ul className="space-y-4">
                {section.links.map((link) => (
                  <li key={link.name}>
                    <a
                      href={link.href}
                      className="text-gray-400 hover:text-primary-400 transition-colors duration-300 text-sm font-medium hover:underline"
                    >
                      {link.name}
                    </a>
                  </li>
                ))}
              </ul>
            </motion.div>
          ))}
        </div>

        {/* Enhanced Bottom Bar */}
        <div className="border-t border-slate-700/50 mt-12 pt-8 flex flex-col sm:flex-row items-center justify-between">
          <div className="flex items-center space-x-2 text-sm text-gray-400 mb-4 sm:mb-0">
            <span>Made with</span>
            <Heart className="w-4 h-4 text-red-400 animate-pulse" />
            <span>for hackathons</span>
          </div>
          
          <div className="text-sm text-gray-400">
            © 2024 AI Mentor. All rights reserved.
          </div>
        </div>
      </div>
    </footer>
  );
}