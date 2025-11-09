from typing import List, Dict  # Pastikan import ini ada
from models.content_models import GeneratedContent, PostResult
from services.circlo_api import CircloAPI


class PostManager:
    def __init__(self):
        self.circlo_api = CircloAPI()

    def post_content_to_circlo(self, content_list: List[GeneratedContent]) -> List[PostResult]:
        """Post generated content to Circlo"""
        print("📮 Posting content to Circlo...")

        results = []

        for content in content_list:
            post_data = {
                "media_type": content.content_type,
                "media_source": content.media_source,
                "caption": content.caption,
                "keywords": content.keywords[:8],  # Limit to 8 keywords
                "niche": "Tech Reviewer"  # Default niche
            }

            result = self.circlo_api.create_post(post_data)
            results.append(result)

            if result.success:
                print(f"✅ Successfully posted {content.content_type} (ID: {result.post_id})")
            else:
                print(f"❌ Failed to post {content.content_type}")

        return results

    def generate_analytics_report(self,
                                  content_created: List[GeneratedContent],
                                  post_results: List[PostResult]) -> Dict:
        """Generate analytics report for the content cycle"""
        successful_posts = [r for r in post_results if r.success]
        failed_posts = [r for r in post_results if not r.success]

        total_viral_score = sum(content.viral_score for content in content_created)
        avg_viral_score = total_viral_score / len(content_created) if content_created else 0

        return {
            "campaign_id": f"ACF_{hash(str(content_created))}",
            "timestamp": post_results[0].posted_at if post_results else None,
            "performance": {
                "total_content_created": len(content_created),
                "successful_posts": len(successful_posts),
                "failed_posts": len(failed_posts),
                "success_rate": len(successful_posts) / len(post_results) if post_results else 0,
                "average_viral_score": avg_viral_score,
                "total_trends_used": len(set([kw for content in content_created for kw in content.trend_alignment]))
            },
            "recommendations": {
                "next_cycle_improvements": [
                    "Increase video content ratio",
                    "Add more interactive elements",
                    "Experiment with different content formats"
                ]
            }
        }