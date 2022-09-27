package com.yr.huajian.manager;

import android.animation.Animator;
import android.animation.AnimatorSet;
import android.animation.ObjectAnimator;
import android.content.Context;
import android.view.View;
import android.widget.FrameLayout;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.fragment.app.FragmentActivity;

import com.bumptech.glide.Glide;
import com.netease.nim.uikit.model.ZonePkUserVo;
import com.yr.common.tools.ScreenUtils;
import com.yr.common.tools.glide.GlideUtil;
import com.yr.huajian.R;

import java.util.List;
import java.util.concurrent.TimeUnit;

import io.reactivex.Observable;
import io.reactivex.android.schedulers.AndroidSchedulers;
import io.reactivex.disposables.Disposable;
import io.reactivex.schedulers.Schedulers;

/**
 * Created by H_XIAO on 2018/9/26.
 * 不建议使用，会有内存泄漏的问题
 */
@Deprecated
public class AnimManager {
    private static volatile AnimManager mInstance;

    public static AnimManager getInstance() {
        if (mInstance == null) {
            synchronized (AnimManager.class) {
                if (mInstance == null) {
                    mInstance = new AnimManager();
                }
            }
        }
        return mInstance;
    }

    public AnimManager() {

    }




    /**********************************1V1视频聊PK动画*************************************/
    private View mChatPkView;
    private AnimatorSet mChatPkSet1;
    private AnimatorSet mChatPkSet2;
    private Disposable mChatPkDelayDisposable;

    /**
     * 展示视频聊PK动画
     * @param view
     * @param list
     */
    public void showChatPkAnim(View view, List<ZonePkUserVo> list){
        this.mChatPkView = view;
        if (mChatPkView == null || list == null || list.size() < 2) {
            return;
        }
        ZonePkUserVo dataLeft = list.get(0);
        ZonePkUserVo dataRight = list.get(1);
        FrameLayout pkLeft = (FrameLayout) view.findViewById(R.id.anim_left);
        FrameLayout pkRight = (FrameLayout) view.findViewById(R.id.anim_right);
        ImageView vs = (ImageView) view.findViewById(R.id.anim_vs);
        ImageView imgLeft = (ImageView) view.findViewById(R.id.img_left);
        ImageView imgRight = (ImageView) view.findViewById(R.id.img_right);
        TextView nameLeft = (TextView) view.findViewById(R.id.name_left);
        TextView nameRight = (TextView) view.findViewById(R.id.name_right);

        vs.setVisibility(View.GONE);
        mChatPkView.setVisibility(View.VISIBLE);

        nameLeft.setText(dataLeft.nickname);
        nameRight.setText(dataRight.nickname);
        GlideUtil.load(dataLeft.avatar, imgLeft, R.mipmap.online_default_header);
        GlideUtil.load(dataRight.avatar, imgRight, R.mipmap.online_default_header);

        ObjectAnimator leftIn = ObjectAnimator.ofFloat(pkLeft, "translationX", -ScreenUtils.getScreenWidth() * 2 / 3f, 0F);
        ObjectAnimator rightIn = ObjectAnimator.ofFloat(pkRight, "translationX", ScreenUtils.getScreenWidth() * 2 / 3f, 0F);
//        leftIn.setInterpolator(new BounceInterpolator());
//        rightIn.setInterpolator(new BounceInterpolator());
        ObjectAnimator pkIn1 = ObjectAnimator.ofFloat(vs, "scaleX", 0f, 1F);
        ObjectAnimator pkIn2 = ObjectAnimator.ofFloat(vs, "scaleY", 0f, 1F);
        ObjectAnimator pkIn3 = ObjectAnimator.ofFloat(vs, "alpha", 0f, 1f);

        pkIn1.addListener(new Animator.AnimatorListener() {
            @Override
            public void onAnimationStart(Animator animation) {
                if (vs != null) {
                    vs.setVisibility(View.VISIBLE);
                }
            }

            @Override
            public void onAnimationEnd(Animator animation) {
                mChatPkDelayDisposable = Observable.timer(2, TimeUnit.SECONDS)
                        .subscribeOn(Schedulers.newThread())
                        .observeOn(AndroidSchedulers.mainThread())
                        .subscribe(aLong -> {
                            if (mChatPkView != null) {
                                mChatPkView.setVisibility(View.GONE);
                            }
                        }, throwable -> {

                        });
            }

            @Override
            public void onAnimationCancel(Animator animation) {

            }

            @Override
            public void onAnimationRepeat(Animator animation) {

            }
        });
        mChatPkSet1 = new AnimatorSet();
        mChatPkSet2 = new AnimatorSet();
        mChatPkSet1.play(leftIn).with(rightIn);
        mChatPkSet1.setDuration(600);
        mChatPkSet1.start();
        mChatPkSet2.play(pkIn1).with(pkIn2).with(pkIn3);
        mChatPkSet2.setStartDelay(400);
        mChatPkSet2.setDuration(200);
        mChatPkSet2.start();
    }

    /**
     * 取消视频聊PK动画
     */
    public void destoryChatPkAnim() {
        destroyChatPkDelayDisposable();
        if (mChatPkView != null) {
            mChatPkView.clearAnimation();
        }
        if (mChatPkSet1 != null) {
            mChatPkSet1.cancel();
        }
        if (mChatPkSet2 != null) {
            mChatPkSet2.cancel();
        }
        mChatPkView = null;
    }

    private void destroyChatPkDelayDisposable() {
        if (mChatPkDelayDisposable != null && !mChatPkDelayDisposable.isDisposed()) {
            mChatPkDelayDisposable.dispose();
            mChatPkDelayDisposable = null;
        }
    }
    /**********************************1V1视频聊PK动画*************************************/


    /**********************************PK动画*************************************/
    private View pkView;
    private AnimatorSet set1;
    private AnimatorSet set2;
    private Disposable delayDisposable;

    public void destoryPkAnim() {
        destroyDelayDisposable();
        if (pkView != null) {
            pkView.clearAnimation();
        }
        if (set1 != null) {
            set1.cancel();
        }
        if (set2 != null) {
            set2.cancel();
        }
        pkView = null;
    }

    private void destroyDelayDisposable() {
        if (delayDisposable != null && !delayDisposable.isDisposed()) {
            delayDisposable.dispose();
            delayDisposable = null;
        }
    }

    public void showPkAnim(View view, List<ZonePkUserVo> list) {
        this.pkView = view;
        if (pkView == null || list == null || list.size() < 2) {
            return;
        }
        ZonePkUserVo dataLeft = list.get(0);
        ZonePkUserVo dataRight = list.get(1);
        FrameLayout pkLeft = (FrameLayout) view.findViewById(R.id.anim_left);
        FrameLayout pkRight = (FrameLayout) view.findViewById(R.id.anim_right);
        ImageView vs = (ImageView) view.findViewById(R.id.anim_vs);
        ImageView imgLeft = (ImageView) view.findViewById(R.id.img_left);
        ImageView imgRight = (ImageView) view.findViewById(R.id.img_right);
        TextView nameLeft = (TextView) view.findViewById(R.id.name_left);
        TextView nameRight = (TextView) view.findViewById(R.id.name_right);
        TextView tagLeft = (TextView) view.findViewById(R.id.tag_left);
        TextView tagRight = (TextView) view.findViewById(R.id.tag_right);
        tagLeft.setVisibility(View.GONE);
        tagRight.setVisibility(View.GONE);
        vs.setVisibility(View.GONE);
        pkView.setVisibility(View.VISIBLE);
        if (dataLeft.winningStreak > 0) {
            tagLeft.setVisibility(View.VISIBLE);
            tagLeft.setText(dataLeft.winningStreak + "连胜");
        }
        if (dataRight.winningStreak > 0) {
            tagRight.setVisibility(View.VISIBLE);
            tagRight.setText(dataRight.winningStreak + "连胜");
        }
        nameLeft.setText(dataLeft.nickname);
        nameRight.setText(dataRight.nickname);
        Context context = imgLeft.getContext();
        //Buggly 上 You cannot start a load for a destroyed activity 问题
        if (context != null && context instanceof FragmentActivity && !((FragmentActivity)context).isFinishing() && !((FragmentActivity)context).isDestroyed()){
            Glide.with(imgLeft.getContext()).load(dataLeft.avatar).into(imgLeft);
            Glide.with(imgRight.getContext()).load(dataRight.avatar).into(imgRight);
        }

        ObjectAnimator leftIn = ObjectAnimator.ofFloat(pkLeft, "translationX", -ScreenUtils.getScreenWidth() * 2 / 3f, 0F);
        ObjectAnimator rightIn = ObjectAnimator.ofFloat(pkRight, "translationX", ScreenUtils.getScreenWidth() * 2 / 3f, 0F);
//        leftIn.setInterpolator(new BounceInterpolator());
//        rightIn.setInterpolator(new BounceInterpolator());
        ObjectAnimator pkIn1 = ObjectAnimator.ofFloat(vs, "scaleX", 0f, 1F);
        ObjectAnimator pkIn2 = ObjectAnimator.ofFloat(vs, "scaleY", 0f, 1F);
        ObjectAnimator pkIn3 = ObjectAnimator.ofFloat(vs, "alpha", 0f, 1f);

        pkIn1.addListener(new Animator.AnimatorListener() {
            @Override
            public void onAnimationStart(Animator animation) {
                if (vs != null) {
                    vs.setVisibility(View.VISIBLE);
                }
            }

            @Override
            public void onAnimationEnd(Animator animation) {
                delayDisposable = Observable.timer(2, TimeUnit.SECONDS)
                        .subscribeOn(Schedulers.newThread())
                        .observeOn(AndroidSchedulers.mainThread())
                        .subscribe(aLong -> {
                            if (pkView != null) {
                                pkView.setVisibility(View.GONE);
                            }
                        }, throwable -> {

                        });
            }

            @Override
            public void onAnimationCancel(Animator animation) {

            }

            @Override
            public void onAnimationRepeat(Animator animation) {

            }
        });
        set1 = new AnimatorSet();
        set2 = new AnimatorSet();
        set1.play(leftIn).with(rightIn);
        set1.setDuration(600);
        set1.start();
        set2.play(pkIn1).with(pkIn2).with(pkIn3);
        set2.setStartDelay(400);
        set2.setDuration(200);
        set2.start();
    }

    /**********************************摇一摇动画*************************************/
    public void showYYYAnim(View topView, View bottomView, OnAnimListener listener) {
        ObjectAnimator top = ObjectAnimator.ofFloat(topView, "translationY", 0, -ScreenUtils.getScreenWidth() / 3f, 0);
        ObjectAnimator bottom = ObjectAnimator.ofFloat(bottomView, "translationY", 0, ScreenUtils.getScreenWidth() / 3f, 0);
        top.addListener(new Animator.AnimatorListener() {
            @Override
            public void onAnimationStart(Animator animation) {
            }

            @Override
            public void onAnimationEnd(Animator animation) {
                listener.onAnimFinish();
            }

            @Override
            public void onAnimationCancel(Animator animation) {

            }

            @Override
            public void onAnimationRepeat(Animator animation) {

            }
        });


        set1 = new AnimatorSet();
        set2 = new AnimatorSet();
        set1.play(top);
        set1.setDuration(1800);
        set1.start();
        set2.play(bottom);
        set2.setDuration(1800);
        set2.start();
    }


    private AnimatorSet set3;
    private AnimatorSet set4;

    public void showGiftInfoAnim(final View item, final View viewImg, final View viewBg, final View name, final View desc, OnAnimListener listener) {
        viewImg.setVisibility(View.INVISIBLE);
        viewBg.setVisibility(View.INVISIBLE);
        name.setVisibility(View.INVISIBLE);
        desc.setVisibility(View.INVISIBLE);
        ObjectAnimator top1 = ObjectAnimator.ofFloat(viewImg, "scaleX", 0f, 1.3f, 0.9f, 1.1f, 1f);
        ObjectAnimator top2 = ObjectAnimator.ofFloat(viewImg, "scaleY", 0f, 1.3f, 0.9f, 1.1f, 1f);
        ObjectAnimator bg = ObjectAnimator.ofFloat(viewBg, "rotationX", 0, 360);
        ObjectAnimator left = ObjectAnimator.ofFloat(name, "translationX", -ScreenUtils.getScreenWidth() * 2 / 3f, 0F);
        ObjectAnimator right = ObjectAnimator.ofFloat(desc, "translationX", ScreenUtils.getScreenWidth() * 2 / 3f, 0F);
        ObjectAnimator out1 = ObjectAnimator.ofFloat(item, "rotation", 0, 3600);
        ObjectAnimator out2 = ObjectAnimator.ofFloat(item, "scaleX", 1f, 1.1f, 0f);
        ObjectAnimator out3 = ObjectAnimator.ofFloat(item, "scaleY", 1f, 1.1f, 0f);
        ObjectAnimator out4 = ObjectAnimator.ofFloat(item, "translationX", 0, -100, ScreenUtils.getScreenWidth() / 2f);
        ObjectAnimator out5 = ObjectAnimator.ofFloat(item, "translationY", 0, 100, -ScreenUtils.getScreenWidth() / 2f);
        set1 = new AnimatorSet();
        set2 = new AnimatorSet();
        set3 = new AnimatorSet();
        set4 = new AnimatorSet();
        top1.addListener(new Animator.AnimatorListener() {
            @Override
            public void onAnimationStart(Animator animation) {
                viewImg.setVisibility(View.VISIBLE);
            }

            @Override
            public void onAnimationEnd(Animator animation) {

            }

            @Override
            public void onAnimationCancel(Animator animation) {

            }

            @Override
            public void onAnimationRepeat(Animator animation) {

            }
        });
        left.addListener(new Animator.AnimatorListener() {
            @Override
            public void onAnimationStart(Animator animation) {
                name.setVisibility(View.VISIBLE);
                desc.setVisibility(View.VISIBLE);
                viewBg.setVisibility(View.VISIBLE);
            }

            @Override
            public void onAnimationEnd(Animator animation) {

            }

            @Override
            public void onAnimationCancel(Animator animation) {

            }

            @Override
            public void onAnimationRepeat(Animator animation) {

            }
        });
        set1.play(top1).with(top2);
        set1.setStartDelay(2200);
        set1.setDuration(1200);
        set1.start();

        set2.play(bg);
        set2.setStartDelay(1000);
        set2.setDuration(800);
        set2.start();

        set3.play(left).with(right);
        set3.setStartDelay(1000);
        set3.setDuration(1200);
        set3.start();

        set4.play(out5).with(out2).with(out3).with(out4);
        set4.setStartDelay(6000);
        set4.setDuration(1000);
        set4.start();
    }

    /**********************************视频聊天输入框隐藏动画*************************************/
    public void showEditGoneAnim(View view, long duration, OnAnimListener listener) {
        ObjectAnimator animator = ObjectAnimator.ofFloat(view, "alpha", 1f, 0f, 1f);
        animator.addListener(new Animator.AnimatorListener() {
            @Override
            public void onAnimationStart(Animator animation) {
            }

            @Override
            public void onAnimationEnd(Animator animation) {
                if (listener != null) {
                    listener.onAnimFinish();
                }
            }

            @Override
            public void onAnimationCancel(Animator animation) {

            }

            @Override
            public void onAnimationRepeat(Animator animation) {

            }
        });
        animator.start();
    }

    /**********************************导播模式 等待中动画*************************************/
    public void showGuideWaitAnim(View group, View animView, OnAnimListener listener) {
        set1 = new AnimatorSet();
        set2 = new AnimatorSet();
        set3 = new AnimatorSet();
        ObjectAnimator animator1 = ObjectAnimator.ofFloat(animView, "scaleX", 0, 0.7f);
        ObjectAnimator animator2 = ObjectAnimator.ofFloat(animView, "scaleY", 0, 0.7f);
        ObjectAnimator animator3 = ObjectAnimator.ofFloat(animView, "scaleX", 0.7f, 1f, 0.7f, 1f);
        ObjectAnimator animator4 = ObjectAnimator.ofFloat(animView, "scaleY", 0.7f, 1f, 0.7f, 1f);
        ObjectAnimator animator5 = ObjectAnimator.ofFloat(animView, "scaleX", 1f, 0);
        ObjectAnimator animator6 = ObjectAnimator.ofFloat(animView, "scaleY", 1f, 0);
        animator1.addListener(new Animator.AnimatorListener() {
            @Override
            public void onAnimationStart(Animator animation) {
                group.setVisibility(View.VISIBLE);
            }

            @Override
            public void onAnimationEnd(Animator animation) {
            }

            @Override
            public void onAnimationCancel(Animator animation) {
            }

            @Override
            public void onAnimationRepeat(Animator animation) {
            }
        });
        animator5.addListener(new Animator.AnimatorListener() {
            @Override
            public void onAnimationStart(Animator animation) {
                group.setVisibility(View.VISIBLE);
            }

            @Override
            public void onAnimationEnd(Animator animation) {
                group.setVisibility(View.GONE);
                if (listener != null) {
                    listener.onAnimFinish();
                }
            }

            @Override
            public void onAnimationCancel(Animator animation) {
            }

            @Override
            public void onAnimationRepeat(Animator animation) {
            }
        });
        set1.play(animator1).with(animator2);
        set1.setDuration(500);
        set1.start();
        set2.play(animator3).with(animator4);
        set2.setStartDelay(500);
        set2.setDuration(2000);
        set2.start();
        set3.play(animator5).with(animator6);
        set3.setStartDelay(2500);
        set3.setDuration(500);
        set3.start();
    }

    public void showAlphaAnim(View view, long duration, OnAnimListener listener) {
        ObjectAnimator animator = ObjectAnimator.ofFloat(view, "alpha", 0f, 1f);
        animator.addListener(new Animator.AnimatorListener() {
            @Override
            public void onAnimationStart(Animator animation) {
                view.setVisibility(View.VISIBLE);
            }

            @Override
            public void onAnimationEnd(Animator animation) {
                if (listener != null) {
                    listener.onAnimFinish();
                }
            }

            @Override
            public void onAnimationCancel(Animator animation) {

            }

            @Override
            public void onAnimationRepeat(Animator animation) {

            }
        });
        animator.setDuration(duration);
        animator.start();
    }

    public void showLiveAnim(View viewBorder, View viewAvatar) {
        set1 = new AnimatorSet();
        set2 = new AnimatorSet();
        ObjectAnimator animator = ObjectAnimator.ofFloat(viewBorder, "alpha", 1f, 0f, 0f);
        ObjectAnimator animator1 = ObjectAnimator.ofFloat(viewBorder, "scaleX", 1f, 1.18f, 1.18f);
        ObjectAnimator animator2 = ObjectAnimator.ofFloat(viewBorder, "scaleY", 1f, 1.18f, 1.18f);
        ObjectAnimator animator3 = ObjectAnimator.ofFloat(viewAvatar, "scaleX", 1f, 0.8f, 1f);
        ObjectAnimator animator4 = ObjectAnimator.ofFloat(viewAvatar, "scaleY", 1f, 0.8f, 1f);
        animator.setRepeatCount(-1);
        animator1.setRepeatCount(-1);
        animator2.setRepeatCount(-1);
        animator3.setRepeatCount(-1);
        animator4.setRepeatCount(-1);
        set1.setDuration(800);
        set2.setDuration(800);
        set1.play(animator).with(animator1).with(animator2);
        set2.play(animator3).with(animator4);
        set1.start();
        set2.start();
    }

    public void showApmVoiceAnim(View viewBorder1, View viewBorder2) {
        showVoiceAnim(viewBorder1, viewBorder2, 1.2f);
    }

    public void showOLVoiceAnim(View viewBorder1, View viewBorder2) {
        showVoiceAnim(viewBorder1, viewBorder2, 1.3f);
    }

    public void showVoiceAnim(View viewBorder1, View viewBorder2, float scale) {
        set1 = new AnimatorSet();
        set2 = new AnimatorSet();
        ObjectAnimator animator = ObjectAnimator.ofFloat(viewBorder1, "alpha", 0f, 0.3f, 0.6f, 0.5f, 0.4f, 0.3f, 0.2f, 0.1f, 0f);
        ObjectAnimator animator1 = ObjectAnimator.ofFloat(viewBorder1, "scaleX", 1f, scale);
        ObjectAnimator animator2 = ObjectAnimator.ofFloat(viewBorder1, "scaleY", 1f, scale);
        ObjectAnimator animator3 = ObjectAnimator.ofFloat(viewBorder2, "alpha", 0f, 0.3f, 0.6f, 0.5f, 0.4f, 0.3f, 0.2f, 0.1f, 0f);
        ObjectAnimator animator4 = ObjectAnimator.ofFloat(viewBorder2, "scaleX", 1f, scale);
        ObjectAnimator animator5 = ObjectAnimator.ofFloat(viewBorder2, "scaleY", 1f, scale);
        animator.setRepeatCount(0);
        animator1.setRepeatCount(0);
        animator2.setRepeatCount(0);
        animator3.setRepeatCount(0);
        animator4.setRepeatCount(0);
        animator5.setRepeatCount(0);
        animator.addListener(new Animator.AnimatorListener() {
            @Override
            public void onAnimationStart(Animator animation) {
                viewBorder1.setVisibility(View.VISIBLE);
            }

            @Override
            public void onAnimationEnd(Animator animation) {
                viewBorder1.setVisibility(View.GONE);
            }

            @Override
            public void onAnimationCancel(Animator animation) {
            }

            @Override
            public void onAnimationRepeat(Animator animation) {
            }
        });
        animator3.addListener(new Animator.AnimatorListener() {
            @Override
            public void onAnimationStart(Animator animation) {
                viewBorder2.setVisibility(View.VISIBLE);
            }

            @Override
            public void onAnimationEnd(Animator animation) {
                viewBorder2.setVisibility(View.GONE);
            }

            @Override
            public void onAnimationCancel(Animator animation) {

            }

            @Override
            public void onAnimationRepeat(Animator animation) {

            }
        });
        set1.setDuration(1000);
        set2.setDuration(1000);
        set2.setStartDelay(500);
        set1.play(animator).with(animator1).with(animator2);
        set2.play(animator3).with(animator4).with(animator5);
        set1.start();
        set2.start();
    }


    public static void cancel(@Nullable final int aaa, TextView view){
        destroyDelayDisposable();
        if(set1 != null){
            set1.cancel();
        }
        if(set2 != null){
            set2.cancel();
        }
        if(set3 != null){
            set3.cancel();
        }
        if(set4 != null){
            set4.cancel();
        }
    }

    public interface OnAnimListener
    {
        void onAnimStart();

        void onAnimFinish();
    }
}








































































