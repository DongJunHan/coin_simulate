

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <stdbool.h>
#include <stdint.h>


typedef int64_t		ArrayIndex;

void
get_basic_candles(
		double		open_array[],
		double		high_array[],
		double		low_array[],
		double		close_array[],
		double		volume_array[],
		int			delimiter_array[],
		ArrayIndex	count,
		double		ret_open_array[],
		double		ret_high_array[],
		double		ret_low_array[],
		double		ret_close_array[],
		double		ret_volume_array[]
) {

	ArrayIndex	last_delim_index = 0;

	bool	first_flag = true;
	double	acc_open   = 0;
	double	acc_high   = 0;
	double	acc_low    = 0;
	double	acc_close  = 0;
	double	acc_volume = 0;

	for (ArrayIndex index = 0; index < count; index++) {

		int delim = delimiter_array[index];

		if (delim == 1) {
			for (ArrayIndex local_index = last_delim_index;
					local_index < index; local_index++) {
				ret_open_array[local_index] = acc_open;
				ret_high_array[local_index] = acc_high;
				ret_low_array[local_index] = acc_low;
				ret_close_array[local_index] = acc_close;
				ret_volume_array[local_index] = acc_volume;
			}
			last_delim_index = index;

			first_flag = true;
			acc_open   = 0;
			acc_high   = 0;
			acc_low    = 0;
			acc_close  = 0;
			acc_volume = 0;
		}

		if (first_flag == true)
			acc_open = open_array[index];
		if (acc_high < high_array[index])
			acc_high = high_array[index];
		if (first_flag == true)
			acc_low = low_array[index];
		if (acc_low > low_array[index])
			acc_low = low_array[index];
		acc_close = close_array[index];
		acc_volume += volume_array[index];

		first_flag = false;
	}

	for (ArrayIndex index = last_delim_index; index < count; index++) {
		ret_open_array[index] = acc_open;
		ret_high_array[index] = acc_high;
		ret_low_array[index] = acc_low;
		ret_close_array[index] = acc_close;
		ret_volume_array[index] = acc_volume;
	}
}


void
get_basic_candles_realtime(
		double		open_array[],
		double		high_array[],
		double		low_array[],
		double		close_array[],
		double		volume_array[],
		int			delimiter_array[],
		ArrayIndex	count,
		double		ret_open_array[],
		double		ret_high_array[],
		double		ret_low_array[],
		double		ret_close_array[],
		double		ret_volume_array[]
) {

	bool	first_flag = true;
	double	acc_open   = 0;
	double	acc_high   = 0;
	double	acc_low    = 0;
	double	acc_close  = 0;
	double	acc_volume = 0;

	for (ArrayIndex index = 0; index < count; index++) {

		int delim = delimiter_array[index];

		if (delim == 1) {
			first_flag = true;
			acc_open   = 0;
			acc_high   = 0;
			acc_low    = 0;
			acc_close  = 0;
			acc_volume = 0;
		} else {
			if (index - 1 >= 0) {
				if (first_flag == true)
					acc_open = open_array[index - 1];
				if (acc_high < high_array[index - 1])
					acc_high = high_array[index - 1];
				if (first_flag == true)
					acc_low = low_array[index - 1];
				if (acc_low > low_array[index - 1])
					acc_low = low_array[index - 1];
				acc_close = close_array[index - 1];
				acc_volume += volume_array[index - 1];
				first_flag = false;
			}
		}
		if (first_flag == true)
			acc_open = open_array[index];
		if (acc_high < open_array[index])
			acc_high = open_array[index];
		if (first_flag == true)
			acc_low = open_array[index];
		if (acc_low > open_array[index])
			acc_low = open_array[index];
		acc_close = open_array[index];
		acc_volume += 0;
		first_flag = false;

		ret_open_array[index] = acc_open;
		ret_high_array[index] = acc_high;
		ret_low_array[index] = acc_low;
		ret_close_array[index] = acc_close;
		ret_volume_array[index] = acc_volume;
	}
}





/*
 * Exponetial Moving Average
 */
void
get_ema_adjust(
		double		data_array[],
		int			delimiter_array[],
		ArrayIndex	count,
		int			indicator,
		double		ret_ema_array[]
) {
	double coefficient =  2.0 / ((double) 1.0 + indicator);
	double ema_y = 1.0;
	double ema_x = 1.0;

	for (ArrayIndex i = 0; i < count; i++) {
		double data = data_array[i];

		if(i == 0){
			ema_x = data;
			ema_y = 1;
		} else {
			if (delimiter_array[i] == 1) {
				ema_x = ema_x * (1 - coefficient) + data;
				ema_y = 1 + (ema_y * (1 - coefficient));
			}
		}

		double ema_data = ema_x / ema_y;
		ret_ema_array[i] = ema_data;
	}
}


/*
 * Exponetial Moving Average for realtime
 */
void
get_ema_adjust_realtime(
		double		data_array[],
		double		realtime_data_array[],
		int			delimiter_array[],
		ArrayIndex	count,
		int			indicator,
		double		ret_ema_array[]
) {
	double coefficient =  2.0 / ((double) 1.0 + indicator);
	double last_ema_y = 0.0;
	double last_ema_x = 0.0;
	double ema_y;
	double ema_x;

	for (ArrayIndex i = 0; i < count; i++) {
		double data = realtime_data_array[i];

		if (delimiter_array[i] == 1) {
			if (i != 0) {
				double last_data = data_array[i - 1];

				last_ema_x = last_ema_x * (1 - coefficient) + last_data;
				last_ema_y = 1 + (last_ema_y * (1 - coefficient));
			}
		}
		ema_x = last_ema_x * (1 - coefficient) + data;
		ema_y = 1 + (last_ema_y * (1 - coefficient));

		double ema_data = ema_x / ema_y;
		ret_ema_array[i] = ema_data;
	}
}

void
get_macd(
		double		data_array[],
		int			delimiter_array[],
		ArrayIndex	count,
		int			macd_fast,
		int			macd_slow,
		double		ret_macd_array[]
) {

	double* ema_fast = (double*) malloc(sizeof(double) * count);
	double* ema_slow = (double*) malloc(sizeof(double) * count);

	get_ema_adjust(
			data_array,
			delimiter_array,
			count,
			macd_fast,
			ema_fast
	);
	get_ema_adjust(
			data_array,
			delimiter_array,
			count,
			macd_slow,
			ema_slow
	);

	for (ArrayIndex i = 0; i < count; i++) {
		double macd = ema_fast[i] - ema_slow[i];
		ret_macd_array[i] = macd;
	}

	free(ema_fast);
	free(ema_slow);
}

void
get_macd_realtime(
		double		data_array[],
		double		realtime_data_array[],
		int			delimiter_array[],
		ArrayIndex	count,
		int			macd_fast,
		int			macd_slow,
		double		ret_macd_array[]
) {

	double* ema_fast = (double*) malloc(sizeof(double) * count);
	double* ema_slow = (double*) malloc(sizeof(double) * count);

	get_ema_adjust_realtime(
			data_array,
			realtime_data_array,
			delimiter_array,
			count,
			macd_fast,
			ema_fast
	);
	get_ema_adjust_realtime(
			data_array,
			realtime_data_array,
			delimiter_array,
			count,
			macd_slow,
			ema_slow
	);

	for (ArrayIndex i = 0; i < count; i++) {
		double macd = ema_fast[i] - ema_slow[i];
		ret_macd_array[i] = macd;
	}

	free(ema_fast);
	free(ema_slow);
}



void
get_macd_signal(
		double		data_array[],
		int			delimiter_array[],
		ArrayIndex	count,
		int			macd_fast,
		int			macd_slow,
		int			signal,
		double		ret_macd_signal_array[]
) {

	double* macd = (double*) malloc(sizeof(double) * count);

	get_macd(
			data_array,
			delimiter_array,
			count,
			macd_fast,
			macd_slow,
			macd
	);

	get_ema_adjust(
			macd,
			delimiter_array,
			count,
			signal,
			ret_macd_signal_array
	);

	free(macd);
}


void
get_macd_signal_realtime(
		double		data_array[],
		double		realtime_data_array[],
		int			delimiter_array[],
		ArrayIndex	count,
		int			macd_fast,
		int			macd_slow,
		int			signal,
		double		ret_macd_signal_array[]
) {

	double* macd = (double*) malloc(sizeof(double) * count);
	double* realtime_macd = (double*) malloc(sizeof(double) * count);

	get_macd(
			data_array,
			delimiter_array,
			count,
			macd_fast,
			macd_slow,
			macd
	);
	get_macd_realtime(
			data_array,
			realtime_data_array,
			delimiter_array,
			count,
			macd_fast,
			macd_slow,
			realtime_macd
	);

	get_ema_adjust_realtime(
			macd,
			realtime_macd,
			delimiter_array,
			count,
			signal,
			ret_macd_signal_array
	);

	free(macd);
	free(realtime_macd);
}


void
get_macd_oscillator(
		double		data_array[],
		int			delimiter_array[],
		ArrayIndex	count,
		int			macd_fast,
		int			macd_slow,
		int			signal,
		double		ret_macd_osc_array[]
) {

	double* macd = (double*) malloc(sizeof(double) * count);
	double* macd_signal = (double*) malloc(sizeof(double) * count);

	get_macd(
			data_array,
			delimiter_array,
			count,
			macd_fast,
			macd_slow,
			macd
	);

	get_ema_adjust(
			macd,
			delimiter_array,
			count,
			signal,
			macd_signal
	);

	for (ArrayIndex i = 0; i < count; i++) {
		ret_macd_osc_array[i] = macd[i] - macd_signal[i];
	}

	free(macd);
	free(macd_signal);
}


void
get_macd_oscillator_realtime(
		double		data_array[],
		double		realtime_data_array[],
		int			delimiter_array[],
		ArrayIndex	count,
		int			macd_fast,
		int			macd_slow,
		int			signal,
		double		ret_macd_osc_array[]
) {

	double* macd = (double*) malloc(sizeof(double) * count);
	double* realtime_macd = (double*) malloc(sizeof(double) * count);
	double* macd_signal = (double*) malloc(sizeof(double) * count);

	get_macd(
			data_array,
			delimiter_array,
			count,
			macd_fast,
			macd_slow,
			macd
	);
	get_macd_realtime(
			data_array,
			realtime_data_array,
			delimiter_array,
			count,
			macd_fast,
			macd_slow,
			realtime_macd
	);

	get_ema_adjust_realtime(
			macd,
			realtime_macd,
			delimiter_array,
			count,
			signal,
			macd_signal
	);

	for (ArrayIndex i = 0; i < count; i++) {
		ret_macd_osc_array[i] = realtime_macd[i] - macd_signal[i];
	}

	free(macd);
	free(realtime_macd);
	free(macd_signal);
}

void
get_macd_signal_and_oscillator(
		double		data_array[],
		int			delimiter_array[],
		ArrayIndex	count,
		int			macd_fast,
		int			macd_slow,
		int			signal,
		double		ret_macd_signal_array[],
		double		ret_macd_osc_array[]
) {

	double* macd = (double*) malloc(sizeof(double) * count);

	get_macd(
			data_array,
			delimiter_array,
			count,
			macd_fast,
			macd_slow,
			macd
	);

	get_ema_adjust(
			macd,
			delimiter_array,
			count,
			signal,
			ret_macd_signal_array
	);

	for (ArrayIndex i = 0; i < count; i++) {
		ret_macd_osc_array[i] = macd[i] - ret_macd_signal_array[i];
	}

	free(macd);
}


void
get_macd_signal_and_oscillator_realtime(
		double		data_array[],
		double		realtime_data_array[],
		int			delimiter_array[],
		ArrayIndex	count,
		int			macd_fast,
		int			macd_slow,
		int			signal,
		double		ret_macd_signal_array[],
		double		ret_macd_osc_array[]
) {

	double* macd = (double*) malloc(sizeof(double) * count);
	double* realtime_macd = (double*) malloc(sizeof(double) * count);

	get_macd(
			data_array,
			delimiter_array,
			count,
			macd_fast,
			macd_slow,
			macd
	);
	get_macd_realtime(
			data_array,
			realtime_data_array,
			delimiter_array,
			count,
			macd_fast,
			macd_slow,
			realtime_macd
	);

	get_ema_adjust_realtime(
			macd,
			realtime_macd,
			delimiter_array,
			count,
			signal,
			ret_macd_signal_array
	);

	for (ArrayIndex i = 0; i < count; i++) {
		ret_macd_osc_array[i] = realtime_macd[i] - ret_macd_signal_array[i];
	}

	free(macd);
	free(realtime_macd);
}


#define FALSE					(0)
#define TRUE					(1)

#define POSITION_NONE			(0)
#define POSITION_LONG			(1)
#define POSITION_SHORT			(2)

#define ACTION_NONE				(0)
#define ACTION_LONG_SET			(1)
#define ACTION_SHORT_SET		(2)
#define ACTION_LONG_CLEAR		(3)
#define ACTION_SHORT_CLEAR		(4)

void
get_one_action_and_position(
		int			sign_long_set,
		int			sign_short_set,
		int			sign_long_clear,
		int			sign_short_clear,
		int			last_position,
		int			past_action,
		int*		ret_position,
		int*		ret_action
) {

		*ret_action = ACTION_NONE;
		*ret_position = last_position;

		if (sign_long_clear == TRUE) {
			if (last_position == POSITION_LONG) {
				*ret_action = ACTION_LONG_CLEAR;
				*ret_position = POSITION_NONE;
			}
		}

		if (sign_short_clear == TRUE) {
			if (last_position == POSITION_SHORT) {
				*ret_action = ACTION_SHORT_CLEAR;
				*ret_position = POSITION_NONE;
			}
		}

		if (sign_long_set == TRUE) {
			if ((last_position == POSITION_NONE)
					|| (last_position == POSITION_SHORT)) {

				if ((past_action == ACTION_NONE)
						|| (past_action == ACTION_SHORT_SET)
						|| (past_action == ACTION_SHORT_CLEAR)) {
					*ret_action = ACTION_LONG_SET;
					*ret_position = POSITION_LONG;
				}
			}
		}

		if (sign_short_set == TRUE) {
			if ((last_position == POSITION_NONE)
					|| (last_position == POSITION_LONG)) {

				if ((past_action == ACTION_NONE)
						|| (past_action == ACTION_LONG_SET)
						|| (past_action == ACTION_LONG_CLEAR)) {
					*ret_action = ACTION_SHORT_SET;
					*ret_position = POSITION_SHORT;
				}
			}
		}
}


void
get_action_and_position(
		int			sign_long_set_array[],
		int			sign_short_set_array[],
		int			sign_long_clear_array[],
		int			sign_short_clear_array[],
		int			sign_past_action_clear_array[],
		ArrayIndex	count,
		int			check_past_action,
		int			ret_last_position_array[],
		int			ret_past_action_array[],
		int			ret_position_array[],
		int			ret_action_array[]
) {

	for (ArrayIndex i = 0; i < count; i++) {
		int sign_long_set = sign_long_set_array[i];
		int sign_short_set = sign_short_set_array[i];
		int sign_long_clear = sign_long_clear_array[i];
		int sign_short_clear = sign_short_clear_array[i];
		int sign_past_action_clear = sign_past_action_clear_array[i];

		int past_action;
		int last_position;

		int action;
		int position;

		if (i == 0) {
			past_action = ACTION_NONE;
		} else {
			past_action = ret_action_array[i - 1];
			if (past_action == ACTION_NONE) {
				past_action = ret_past_action_array[i - 1];
			}
		}
		if (sign_past_action_clear == TRUE) {
			past_action = ACTION_NONE;
		}

		if (i == 0) {
			last_position = POSITION_NONE;
		} else {
			last_position = ret_position_array[i - 1];
		}

		get_one_action_and_position(
				sign_long_set,
				sign_short_set,
				sign_long_clear,
				sign_short_clear,
				last_position,
				check_past_action == TRUE ? past_action : ACTION_NONE,
				&position,
				&action
		);

		ret_last_position_array[i] = last_position;
		ret_past_action_array[i] = past_action;
		ret_position_array[i] = position;
		ret_action_array[i] = action;
	}

}




void
get_balance(
		int			last_position_array[],
		int			action_array[],
		double		price_array[],
		double		low_price_array[],
		double		high_price_array[],
		ArrayIndex	count,
		double		first_balance,
		int			leverage,
		double		fee,
		double		ret_trade_price_array[],
		double		ret_base_balance_array[],
		double		ret_balance_array[],
		double		ret_profit_percent_array[]
) {

	for (ArrayIndex i = 0; i < count; i++) {
		int last_position = last_position_array[i];
		int action = action_array[i];
		double price = price_array[i];
		double low_price = low_price_array[i];
		double high_price = high_price_array[i];

		double last_trade_price;
		double trade_price;
		double base_balance;
		double balance;
		double profit_percent;

		double chungsan_profit_percent;

		if (i == 0) {
			base_balance = first_balance;
		} else {
			base_balance = ret_base_balance_array[i - 1];
		}

		if (i == 0) {
			last_trade_price = 0;
		} else {
			last_trade_price = ret_trade_price_array[i - 1];
		}
		trade_price = last_trade_price;


		profit_percent = 0;
		balance = base_balance;
		if (last_position == POSITION_LONG) {
			profit_percent =
				((price - last_trade_price) / last_trade_price) * 100 * leverage;
			balance = (base_balance + base_balance * profit_percent / 100) * (1 - fee);

			chungsan_profit_percent =
				((low_price - last_trade_price) / last_trade_price) * 100 * leverage;
			if (chungsan_profit_percent <= -100) {
				balance = 0;
				base_balance = 0;
			}
		}
		if (last_position == POSITION_SHORT) {
			profit_percent =
				((last_trade_price - price) / last_trade_price) * 100 * leverage;
			balance = (base_balance + base_balance * profit_percent / 100) * (1 - fee);

			chungsan_profit_percent =
				((last_trade_price - high_price) / last_trade_price) * 100 * leverage;
			if (chungsan_profit_percent <= -100) {
				balance = 0;
				base_balance = 0;
			}
		}



		if (action == ACTION_LONG_CLEAR) {
			trade_price = 0;
			base_balance = balance;
		}
		if (action == ACTION_SHORT_CLEAR) {
			trade_price = 0;
			base_balance = balance;
		}
		if (action == ACTION_LONG_SET) {
			trade_price = price;
			balance = balance * (1 - fee);
			base_balance = balance;
		}
		if (action == ACTION_SHORT_SET) {
			trade_price = price;
			balance = balance * (1 - fee);
			base_balance = balance;
		}


		ret_trade_price_array[i] = trade_price;
		ret_base_balance_array[i] = base_balance;
		ret_balance_array[i] = balance;
		ret_profit_percent_array[i] = profit_percent;
	}

}





